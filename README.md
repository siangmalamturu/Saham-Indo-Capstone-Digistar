# Saham-Indo Sentiment Analysis Chatbot

# Kelompok 1

1. Fathurrahman Azhari
2. Ersa Meilia
3. Adityo Pangestu
4. Annasya Atqia Putri

Program chatbot berbasis Streamlit untuk analisis sentimen pasar saham Indonesia menggunakan fine-tuned GPT-4o Mini model.

## 🎯 Deskripsi

Aplikasi yang menganalisis sentimen berita dan artikel tentang saham Indonesia. Chatbot menggunakan model GPT-4o yang telah dilatih khusus untuk memberikan analisis sentimen dalam format:

- **Sentimen Akhir**: Positive, Negative, atau Neutral
- **Analisis Analis**: Penjelasan detail tentang sentimen

## 📋 Fitur Utama

- **Chat Interface**: Antarmuka percakapan dengan riwayat pesan
- **Analisis Real-time**: Analisis sentimen menggunakan fine-tuned model GPT-4o
- **Pembersihan Data Otomatis**: Text preprocessing dengan penghapusan stopwords dan normalisasi
- **Fallback Analysis**: Analisis cadangan dari dataset jika terjadi error API
- **Statistics Sidebar**: Menampilkan statistik data dan status model
- **Custom Styling**: Desain UI yang bersih dan user-friendly

## 🔧 Requirement

- Python 3.8+
- Streamlit
- OpenAI API (dengan akses fine-tuned model)
- Pandas
- Scikit-learn

## 📦 Instalasi

```bash
# Clone atau download repository
cd Saham-Indo-Capstone-Digistar

# Install dependencies
pip install streamlit pandas scikit-learn openai

# Jalankan aplikasi
streamlit run App.py
```

Aplikasi akan berjalan di `http://localhost:8501`

## 📁 Struktur File

| File               | Keterangan                                |
| ------------------ | ----------------------------------------- |
| `App.py`           | Aplikasi utama Streamlit                  |
| `data_cleaning.py` | Module pembersihan dan preprocessing teks |
| `data.csv`         | Dataset training dengan 3000+ record      |
| `README.md`        | Dokumentasi (file ini)                    |

## 🔑 Setup API Key

1. Dapatkan API key dari OpenAI: https://platform.openai.com/api-keys
2. Set API key di App.py pada baris 59:
   ```python
   openai.api_key = "your-api-key-here"
   ```

## 📊 Dataset

Dataset berisi artikel/berita tentang saham Indonesia dengan kolom:

- **content**: Teks artikel
- **sentiment**: Label sentimen (Positive/Negative/Neutral)

## 💡 Cara Penggunaan

1. Jalankan aplikasi dengan `streamlit run App.py`
2. Ketik pertanyaan atau teks tentang saham di input field
3. Tekan Enter atau klik "Kirim" untuk mendapatkan analisis
4. Lihat hasil analisis sentimen di chat area
5. Cek statistik data di sidebar

## 🤖 Model Fine-tuned

Model yang digunakan:

- **Base Model**: GPT-4o Mini
- **Training**: Fine-tuned untuk sentiment analysis saham Indonesia
- **Temperature**: 0.3 (output konsisten dan deterministic)
- **Max Tokens**: 500

## 📝 Catatan Penting

- Simpan API key dengan aman, jangan commit ke git
- Dataset hanya untuk training dan fallback analysis
- Model memerlukan internet connection untuk API calls
- Rate limit OpenAI API: monitor penggunaan

## 📄 License

Capstone Project Digistar
