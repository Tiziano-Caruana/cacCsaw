import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "counter.db"

def fetch_data():
    """Estrae i dati da visit_log e qr_counter."""
    conn = sqlite3.connect(DB_PATH)
    df_visits = pd.read_sql_query("SELECT * FROM visit_log", conn)
    df_qr_counts = pd.read_sql_query("SELECT * FROM qr_counter", conn)
    conn.close()
    return df_visits, df_qr_counts

def plot_global_visits(df_visits):
    """Grafico degli accessi globali nel tempo."""
    df_global = df_visits[df_visits['visit_type'] == 'global'].copy()
    df_global.loc[:, 'timestamp'] = pd.to_datetime(df_global['timestamp'])
    df_global = df_global.set_index('timestamp').resample('D').size()
    
    plt.figure(figsize=(10, 6))
    plt.plot(df_global.index, df_global.values, marker='o', color='b')
    plt.title("Global Visits Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Visits")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_qr_visits(df_qr_counts):
    """Grafico del numero di accessi per ogni QR code."""
    plt.figure(figsize=(10, 6))
    plt.bar(df_qr_counts['qr_id'], df_qr_counts['count'], color='g')
    plt.title("Total Visits per QR Code")
    plt.xlabel("QR Code ID")
    plt.ylabel("Visit Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_qr_visits_over_time(df_visits):
    """Grafico degli accessi specifici per QR code nel tempo."""
    df_qr = df_visits[df_visits['visit_type'] == 'qr_specific'].copy() 
    df_qr.loc[:, 'timestamp'] = pd.to_datetime(df_qr['timestamp'])
    df_qr = df_qr.set_index('timestamp')
    
    plt.figure(figsize=(12, 8))
    
    for qr_id, group in df_qr.groupby('qr_id'):
        qr_visits_over_time = group.resample('D').size()  # Raccoglie per giorno
        plt.plot(qr_visits_over_time.index, qr_visits_over_time.values, label=f"QR ID: {qr_id}")
    
    plt.title("QR Code Visits Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Visits")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    df_visits, df_qr_counts = fetch_data()
    print(df_visits, df_qr_counts)
    
    plot_global_visits(df_visits)
    plot_qr_visits(df_qr_counts)
    plot_qr_visits_over_time(df_visits)

if __name__ == "__main__":
    main()
