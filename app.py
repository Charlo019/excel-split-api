from flask import Flask, request, send_file
import pandas as pd
import io
import zipfile

app = Flask(__name__)

@app.route('/split', methods=['POST'])
def split_excel():
    uploaded_file = request.files['file']
    df = pd.read_excel(uploaded_file)

    df_2025 = df[df['Year'] == 2025]
    df_2024 = df[df['Year'] == 2024]

    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w') as zf:
        buffer_2025 = io.BytesIO()
        df_2025.to_excel(buffer_2025, index=False)
        zf.writestr("data_2025.xlsx", buffer_2025.getvalue())

        buffer_2024 = io.BytesIO()
        df_2024.to_excel(buffer_2024, index=False)
        zf.writestr("data_2024.xlsx", buffer_2024.getvalue())

    output.seek(0)
    return send_file(output, download_name="split_data.zip", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
