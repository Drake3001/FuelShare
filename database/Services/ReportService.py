import matplotlib.pyplot as plt

from database.session import get_session, engine
import pandas as pd
from sqlalchemy import text
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import os

from datetime import datetime
SQL_QUERY= """WITH period_trips AS (
    SELECT 
        id, 
        distance, 
        fuel_consumed, 
        driver_id,
        duration
    FROM trip
    WHERE period = :period
),

payer_count AS (
    SELECT
        tp.trip_id,
        COUNT(tp.user_id) AS payer_cnt
    FROM trip_payer tp
    JOIN period_trips pt ON tp.trip_id  =  pt.id
    GROUP BY tp.trip_id
),

user_paid_stats AS (
    SELECT
        tp.user_id,
        COUNT(DISTINCT t.id) AS trips_paid,
        SUM(t.distance / pc.payer_cnt) AS total_distance_paid,
        SUM(t.fuel_consumed / pc.payer_cnt) AS total_fuel_paid
    FROM period_trips t
    JOIN trip_payer tp ON tp.trip_id = t.id
    JOIN payer_count pc ON pc.trip_id = t.id
    GROUP BY tp.user_id
),

user_driven_stats AS (
    SELECT
        t.driver_id AS user_id,
        COUNT(DISTINCT t.id) AS trips_driven,
        SUM(t.distance) AS total_distance_driven,
        SUM(t.fuel_consumed) AS total_fuel_driven,
        SUM(t.duration) AS total_minutes_driven 
    FROM period_trips t
    WHERE t.driver_id IS NOT NULL
    GROUP BY t.driver_id
)

SELECT
    u.id AS user_id,
    u.name,
    u.surname,
    
    COALESCE(ups.trips_paid, 0) AS trips_paid,
    COALESCE(ups.total_distance_paid, 0) AS total_distance_paid,
    COALESCE(ups.total_fuel_paid, 0) AS total_fuel_paid,

    COALESCE(uds.trips_driven, 0) AS trips_driven,
    COALESCE(uds.total_distance_driven, 0) AS total_distance_driven,
    COALESCE(uds.total_fuel_driven, 0) AS total_fuel_driven,
    COALESCE(uds.total_minutes_driven, 0) AS total_minutes_driven 

FROM user u
LEFT JOIN user_paid_stats ups ON u.id = ups.user_id
LEFT JOIN user_driven_stats uds ON u.id = uds.user_id

WHERE ups.user_id IS NOT NULL OR uds.user_id IS NOT NULL

ORDER BY u.surname;"""



class ReportService:
    def __init__(self):
        self.documents_paths=[]
        self.documents_dir = "reports"
        self.powerbi_dir = "powerbi"
        if not os.path.exists(self.documents_dir):
            os.makedirs(self.documents_dir)
            print("utworzyłem directory")


    def generate_report(self, period: int, include_ev=False):
        query = text(SQL_QUERY)

        df = pd.read_sql_query(
            query,
            engine,
            params={"period": period}
        )

        df['avg_speed_kmh'] = df['total_distance_driven'] / (df['total_minutes_driven'] / 3600)

        df['avg_consumption_l100'] = df.apply(
            lambda x: (x['total_fuel_driven'] / x['total_distance_driven'] * 100)
            if x['total_distance_driven'] > 0 else 0, axis=1
        )

        df['balance_km'] = df['total_distance_paid'] - df['total_distance_driven']

        df['avg_trip_distance'] = df.apply(
            lambda x: (x['total_distance_driven'] / x['trips_driven'])
            if x['trips_driven'] > 0 else 0, axis=1
        )

        df["label"] = df["name"] + " " + df["surname"] + " (" + df["user_id"].astype(str) + ")"

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.documents_dir}/{self.powerbi_dir}/powerbi_{period}_{timestamp}.csv"
        df.to_csv(filename, index=False, encoding='utf-8')



        categories = ['total_distance_driven', 'avg_consumption_l100', 'avg_speed_kmh', 'total_fuel_paid']
        labels_radar = ['Dystans', 'Ekonomia', 'Prędkość', 'Wkład ($)']

        df_norm = df[categories].copy()
        for col in categories:
            min_val = df_norm[col].min()
            max_val = df_norm[col].max()
            if max_val - min_val != 0:
                df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
            else:
                df_norm[col] = 0.5

        df_norm['avg_consumption_l100'] = 1 - df_norm['avg_consumption_l100']
        df_norm['label'] = df['label']

        filename= f"Period {period}-{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        self.documents_paths.append(filename)

        with PdfPages(os.path.join(self.documents_dir, filename)) as pdf:

            # STRONA 1: OKŁADKA I TABELA ZBIORCZA
            fig = plt.figure(figsize=(11.69, 8.27))

            plt.text(0.5, 0.9, "Raport Tras samochodu",
                     horizontalalignment='center',
                     fontsize=24, fontweight='bold', transform=fig.transFigure)

            plt.text(0.5, 0.85, f"Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                     horizontalalignment='center',
                     fontsize=12, color='gray', transform=fig.transFigure)

            table_cols = ['label', 'trips_driven', 'total_distance_driven', 'avg_consumption_l100']
            table_headers = ['Użytkownik', 'Przejazdy (Kier)', 'Dystans (km)', 'Spalanie (l/100)']

            table_data = df[table_cols].copy()
            table_data['total_distance_driven'] = table_data['total_distance_driven'].round(1)
            table_data['avg_consumption_l100'] = table_data['avg_consumption_l100'].round(1)

            cell_text = []
            for row in table_data.values:
                cell_text.append([str(x) for x in row])

            ax_table = plt.gca()
            ax_table.axis('off')

            table = plt.table(cellText=cell_text,
                              colLabels=table_headers,
                              cellLoc='center',
                              loc='center',
                              bbox=[0.1, 0.3, 0.8, 0.4])

            table.auto_set_font_size(False)
            table.set_fontsize(12)
            table.scale(1, 1.5)

            pdf.savefig(fig)
            plt.close()


            # STRONA 2: AKTYWNOŚĆ (GRID 2x2)
            fig, axes = plt.subplots(2, 2, figsize=(11.69, 8.27))
            fig.suptitle("Aktywność Użytkowników", fontsize=18, y=0.95)

            # 1. Trips Driven
            sns.barplot(data=df, x="label", y="trips_driven", ax=axes[0, 0], palette="viridis")
            axes[0, 0].set_title("Liczba przejazdów (Kierowca)")
            axes[0, 0].set_ylabel("Ilość")
            axes[0, 0].set_xlabel("")

            # 2. Trips Paid
            sns.barplot(data=df, x="label", y="trips_paid", ax=axes[0, 1], palette="viridis")
            axes[0, 1].set_title("Liczba przejazdów (Opłacone)")
            axes[0, 1].set_ylabel("Ilość")
            axes[0, 1].set_xlabel("")

            # 3. Kilometers Driven
            sns.barplot(data=df, x="label", y="total_distance_driven", ax=axes[1, 0], palette="magma")
            axes[1, 0].set_title("Przejechane kilometry")
            axes[1, 0].set_ylabel("Dystans (km)")
            axes[1, 0].set_xlabel("Użytkownik")

            # 4. Time Driven
            sns.barplot(data=df, x="label", y="total_minutes_driven", ax=axes[1, 1], palette="magma")
            axes[1, 1].set_title("Czas spędzony za kierownicą")
            axes[1, 1].set_ylabel("Czas (min)")
            axes[1, 1].set_xlabel("Użytkownik")

            plt.tight_layout(rect=[0, 0, 1, 0.93])
            pdf.savefig(fig)
            plt.close()

            # STRONA 3: PALIWO I EKONOMIA (GRID 2x2)
            fig, axes = plt.subplots(2, 2, figsize=(11.69, 8.27))
            fig.suptitle("Ekonomia i Paliwo", fontsize=18, y=0.95)

            # 1. Fuel Driven
            sns.barplot(data=df, x="label", y="total_fuel_driven", ax=axes[0, 0], palette="Reds")
            axes[0, 0].set_title("Spalona benzyna (Jako kierowca)")
            axes[0, 0].set_ylabel("Litry")
            axes[0, 0].set_xlabel("")

            # 2. Fuel Paid
            sns.barplot(data=df, x="label", y="total_fuel_paid", ax=axes[0, 1], palette="Greens")
            axes[0, 1].set_title("Sfinansowana benzyna (Płatnik)")
            axes[0, 1].set_ylabel("Litry")
            axes[0, 1].set_xlabel("")

            # 3. Avg Consumption
            sns.barplot(data=df, x="label", y="avg_consumption_l100", ax=axes[1, 0], palette="coolwarm")
            axes[1, 0].set_title("Średnie spalanie (l/100km)")
            axes[1, 0].set_ylabel("l/100km")
            axes[1, 0].set_xlabel("Użytkownik")

            # 4. Donut Chart (Udział w kosztach paliwa)
            # Donut chart robimy "ręcznie" na osi
            axes[1, 1].pie(df['total_fuel_paid'], labels=df['label'], autopct='%1.1f%%',
                           startangle=90, pctdistance=0.85, colors=sns.color_palette("pastel"))
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            axes[1, 1].add_artist(centre_circle)
            axes[1, 1].set_title("Udział w kosztach paliwa")

            plt.tight_layout(rect=[0, 0, 1, 0.93])
            pdf.savefig(fig)
            plt.close()

            # STRONA 4: ANALIZA STYLU JAZDY
            fig, axes = plt.subplots(2, 1, figsize=(11.69, 8.27))  # Dwa wykresy jeden pod drugim
            fig.suptitle("Analiza Stylu Jazdy", fontsize=18, y=0.95)

            # 1. Lollipop Chart (Prędkość)
            ax_speed = axes[0]
            ax_speed.stem(df['label'], df['avg_speed_kmh'], basefmt="k-")
            ax_speed.set_ylim(bottom=0)
            ax_speed.set_title('Średnia prędkość przelotowa')
            ax_speed.set_ylabel('Prędkość (km/h)')
            ax_speed.grid(axis='y', linestyle='--', alpha=0.7)

            # 2. Scatterplot (Typologia)
            ax_scatter = axes[1]
            sns.scatterplot(data=df, x="trips_driven", y="total_distance_driven",
                            size="avg_consumption_l100", hue="label", sizes=(50, 400),
                            ax=ax_scatter)
            ax_scatter.set_title("Typologia tras (Wielkość kropki = Spalanie)")
            ax_scatter.set_xlabel("Liczba przejazdów")
            ax_scatter.set_ylabel("Łączny dystans (km)")
            ax_scatter.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

            plt.tight_layout(rect=[0, 0, 1, 0.93])
            pdf.savefig(fig)
            plt.close()

            # STRONA 5: PROFIL KIEROWCY (RADAR)




            N = len(categories)
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]  # Domknięcie pętli

            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)

            colors = sns.color_palette("bright", len(df_norm))

            for idx, (index, row) in enumerate(df_norm.iterrows()):
                values = row[categories].tolist()
                values += values[:1]
                ax.plot(angles, values, linewidth=2, linestyle='solid', label=row['label'], color=colors[idx])
                ax.fill(angles, values, alpha=0.1, color=colors[idx])

            plt.xticks(angles[:-1], labels_radar, size=12)
            ax.set_yticklabels([])
            ax.set_ylim(0, 1.05)

            plt.title("Znormalizowany Profil Kierowcy", size=20, y=1.05)
            plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

            plt.tight_layout()
            pdf.savefig(fig)
            plt.close()

        print(f"Raport zapisano pomyślnie w: {filename}")
        df.to_csv(os.path.join(self.documents_dir, 'df.csv'))





if __name__ == "__main__":
    report = ReportService()
    report.generate_report(2)
