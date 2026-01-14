"""
Data Cleaning Module untuk Saham Indo Chatbot
Mengekstrak fungsi cleaning dari Data_Cleaning_Capstone_DCI.ipynb
"""

import pandas as pd
import re
import os
from typing import Tuple

# ==========================================
# DEFINISI STOPWORDS & FUNGSI CLEANING
# ==========================================
STOPWORDS_ID = {
    'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'untuk', 'pada', 'dengan',
    'adalah', 'saya', 'kamu', 'dia', 'mereka', 'kita', 'akan', 'bisa', 'ada',
    'tidak', 'yg', 'ya', 'aja', 'gak', 'nya', 'kalo', 'kalau', 'udah', 'sudah',
    'bukan', 'tapi', 'tuh', 'dong', 'kok', 'sih', 'gue', 'lu', 'aku', 'apa',
    'bgt', 'banget', 'juga', 'lagi', 'mau', 'sama', 'banyak', 'bikin', 'buat',
    'jadi', 'terus', 'karena', 'seperti', 'atau', 'saat', 'dalam', 'masih',
    'begitu', 'semua', 'bbrp', 'utk', 'sdh', 'dgn', 'dr',
    'lebih', 'kemarin', 'per', 'punya', 'setelah', 'menjadi',
    'secara', 'lalu', 'memang', 'paling','nih','dulu','hingga','sampai','sekarang',
    'apakah','memiliki','kembali','sejak','kinerja','kira','coba','nder'
}

STOPWORDS_SAHAM = {
    'saham', 'harga', 'market', 'indeks', 'lot', 'hari', 'tahun',
    'beli', 'jual', 'hold', 'masuk', 'keluar', 'rekomendasi',
    'bbca', 'bbri', 'bmri', 'bbtn', 'tlkm', 'unvr', 'goto', 'bank', 'bca',
    'bbni', 'hmsp', 'tpia', 'bren', 'byan', 'indf', 'antm', 'asii','amp',
    'bri', 'mandiri', 'brpt', 'chandra', 'asri', 'tuck', 'wong','astra','ggrm',
    'ihsg', 'persero', 'tbk', 'lembar', 'pemegang', 'pbv', 'pukul', 'wib','pt',
    'syariah', 'low kwong','prajogo pangestu','indonesia','prajogo','pangestu','bayan','low',
    'kwong','adro','bisnis','emiten','rokok','unilever','rdtx','sampoerna','produk'
}

ALL_STOPWORDS = STOPWORDS_ID.union(STOPWORDS_SAHAM)


def clean_text(text: str) -> str:
    """
    Membersihkan teks dengan menghapus placeholder, mengubah ke lowercase,
    menghapus karakter non-huruf, dan menghapus stopwords.
    
    Args:
        text: Teks yang akan dibersihkan
        
    Returns:
        Teks yang sudah dibersihkan
    """
    if not isinstance(text, str):
        return ""
    
    # Hapus placeholder
    text = re.sub(r'\[URL\]|\[HASHTAG\]|\[USERNAME\]', '', text)
    
    # Ubah ke lowercase
    text = text.lower()
    
    # Hapus non-huruf (hanya simpan huruf dan spasi)
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    # Hapus spasi berlebihan
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Stopword removal
    tokens = [t for t in text.split() if t not in ALL_STOPWORDS]
    return ' '.join(tokens)


def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """
    Memuat dan membersihkan dataset dari CSV.
    
    Args:
        file_path: Path ke file CSV
        
    Returns:
        DataFrame dengan kolom 'cleaned_text' dan 'Sentiment'
    """
    print(f"Loading data from: {file_path}")
    
    # Cek keberadaan file
    if not os.path.exists(file_path):
        if os.path.exists(os.path.basename(file_path)):
            file_path = os.path.basename(file_path)
        else:
            raise FileNotFoundError(f"File tidak ditemukan: {file_path}")
    
    # Baca CSV
    df = pd.read_csv(file_path)
    
    # Hapus kolom tidak terpakai
    unused_cols = ['Quote Count', 'Reply Count', 'Retweet Count', 
                   'Favorite Count', 'English Translation', 'Tweet Date']
    df = df.drop(columns=[c for c in unused_cols if c in df.columns], errors='ignore')
    
    # Cleaning
    print("Cleaning data...")
    df['cleaned_text'] = df['Sentence'].apply(clean_text)
    
    # Hapus duplikat & data kosong
    df = df.drop_duplicates(subset=['cleaned_text'])
    df = df[df['cleaned_text'].str.strip() != '']
    
    print(f"Data siap. Total baris: {len(df)}")
    return df[['cleaned_text', 'Sentiment']]


def load_data_cached(file_path: str) -> pd.DataFrame:
    """
    Memuat dan cache data cleaning hasil proses.
    Gunakan untuk aplikasi yang membutuhkan data yang sudah dibersihkan.
    
    Args:
        file_path: Path ke file CSV asli
        
    Returns:
        DataFrame dengan data yang sudah dibersihkan
    """
    return load_and_clean_data(file_path)


if __name__ == "__main__":
    # Contoh penggunaan
    df_clean = load_and_clean_data("data.csv")
    print("\nSample data:")
    print(df_clean.head())
    print("\nSentiment distribution:")
    print(df_clean['Sentiment'].value_counts())
