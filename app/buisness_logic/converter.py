from typing import List, Tuple, Dict, Union
import io
from pathlib import Path

from PIL import Image
import csv
import tempfile
import subprocess


class DocumentConverter:
    """
    Класс для конвертации различных форматов документов в PDF
    """

    def __init__(self):
        self.supported_formats = {
            'docx': self._convert_docx,
            'txt': self._convert_txt,
            'png': self._convert_image,
            'jpg': self._convert_image,
            'jpeg': self._convert_image,
            'csv': self._convert_csv,
            'pdf': self._pass_through_pdf
        }

    def convert_documents(
            self,
            documents: List[Dict[str, Union[str, bytes]]]
    ) -> Tuple[List[Dict[str, bytes]], List[str]]:
        """
        Конвертирует список документов в PDF формат

        Args:
            documents: Список словарей с документами
                      Каждый словарь должен содержать:
                      - 'filename': имя файла
                      - 'content': содержимое файла в bytes
                      - 'content_type': MIME-тип файла

        Returns:
            Tuple[List[Dict[str, bytes]], List[str]]:
            - Список успешно конвертированных PDF документов
            - Список ошибок
        """
        converted_documents = []
        errors = []

        for doc in documents:
            try:
                # Получаем расширение файла
                ext = Path(doc['filename']).suffix[1:].lower()

                # Проверяем поддержку формата
                if ext not in self.supported_formats:
                    errors.append(f"Unsupported format: {ext} for file {doc['filename']}")
                    continue

                # Конвертируем документ
                pdf_content = self.supported_formats[ext](doc['content'])

                if pdf_content:
                    converted_documents.append({
                        'filename': f"{Path(doc['filename']).stem}.pdf",
                        'content': pdf_content
                    })
                else:
                    errors.append(f"Conversion failed for {doc['filename']}")

            except Exception as e:
                errors.append(f"Error processing {doc['filename']}: {str(e)}")

        return converted_documents, errors

    def _convert_docx(self, content: bytes) -> bytes:
        """Конвертирует DOCX в PDF"""
        try:
            # Создаем временный файл для docx
            with tempfile.NamedTemporaryFile(suffix='.docx') as temp_docx, \
                    tempfile.NamedTemporaryFile(suffix='.pdf') as temp_pdf:

                # Записываем содержимое во временный файл
                temp_docx.write(content)
                temp_docx.flush()

                # Используем LibreOffice для конвертации
                process = subprocess.run([
                    'soffice',
                    '--headless',
                    '--convert-to',
                    'pdf',
                    '--outdir',
                    Path(temp_pdf.name).parent.as_posix(),
                    temp_docx.name
                ], capture_output=True)

                if process.returncode == 0:
                    # Читаем получившийся PDF
                    with open(Path(temp_pdf.name).parent / f"{Path(temp_docx.name).stem}.pdf", 'rb') as pdf_file:
                        return pdf_file.read()

        except Exception as e:
            raise Exception(f"DOCX conversion failed: {str(e)}")

    def _convert_txt(self, content: bytes) -> bytes:
        """Конвертирует TXT в PDF"""
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        try:
            # Создаем PDF в памяти
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)

            # Декодируем текст
            text = content.decode('utf-8', errors='ignore')

            # Добавляем текст в PDF
            y = 750  # начальная y-координата
            for line in text.split('\n'):
                if y > 50:  # проверка на конец страницы
                    c.drawString(50, y, line)
                    y -= 12
                else:
                    c.showPage()
                    y = 750
                    c.drawString(50, y, line)
                    y -= 12

            c.save()
            return pdf_buffer.getvalue()

        except Exception as e:
            raise Exception(f"Text conversion failed: {str(e)}")

    def _convert_image(self, content: bytes) -> bytes:
        """Конвертирует изображение в PDF"""
        try:
            # Открываем изображение из bytes
            image = Image.open(io.BytesIO(content))

            # Конвертируем в RGB если нужно
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')

            # Создаем PDF в памяти
            pdf_buffer = io.BytesIO()
            image.save(pdf_buffer, 'PDF')
            return pdf_buffer.getvalue()

        except Exception as e:
            raise Exception(f"Image conversion failed: {str(e)}")

    def _convert_csv(self, content: bytes) -> bytes:
        """Конвертирует CSV в PDF"""
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors

        try:
            # Читаем CSV
            csv_content = content.decode('utf-8', errors='ignore')
            csv_reader = csv.reader(io.StringIO(csv_content))
            data = list(csv_reader)

            # Создаем PDF
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer)

            # Создаем таблицу
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            # Строим PDF
            doc.build([table])
            return pdf_buffer.getvalue()

        except Exception as e:
            raise Exception(f"CSV conversion failed: {str(e)}")

    def _pass_through_pdf(self, content: bytes) -> bytes:
        """Пропускает PDF как есть"""
        return content
