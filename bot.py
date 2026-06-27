import os
import time
import telebot as tb
from mensajes import *
from pdf_converter import convert_to_docx, convert_to_pdf, convertir_ppt_to_pdf_linux

# Get token from environment variable
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set!")

bot = tb.TeleBot(TOKEN)

# User state management (simple in-memory storage)
user_states = {}

@bot.message_handler(commands=['start'])
def enviar_mensaje(message):
    bot.reply_to(message, texto_bienvenida)
    bot.reply_to(message, texto_convertir)

@bot.message_handler(commands=['convert'])
def enviar_convertir(message):
    markup = tb.types.InlineKeyboardMarkup(row_width=2)
    itembtn1 = tb.types.InlineKeyboardButton('📄 Convertir PDF a DOCX', callback_data='pdf_a_docx')
    itembtn2 = tb.types.InlineKeyboardButton('📄 Convertir a PDF', callback_data='a_pdf')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Elige una opción:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pdf_a_docx":
        bot.answer_callback_query(call.id, "Opción seleccionada: PDF a DOCX")
        bot.send_message(call.message.chat.id, "📤 Envía el archivo PDF que deseas convertir a DOCX.")
        user_states[call.message.chat.id] = 'pdf_a_docx'
    elif call.data == "a_pdf":
        bot.answer_callback_query(call.id, "Opción seleccionada: Convertir a PDF")
        bot.send_message(call.message.chat.id, "📤 Envía el archivo que deseas convertir a PDF.")
        user_states[call.message.chat.id] = 'a_pdf'

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    chat_id = message.chat.id
    
    # Check if user has selected a conversion type
    if chat_id not in user_states:
        bot.reply_to(message, "⚠️ Primero usa /convert para seleccionar un tipo de conversión.")
        return
    
    conversion_type = user_states[chat_id]
    
    try:
        # Check file size (Telegram limit is 20MB)
        if message.document.file_size > 20 * 1024 * 1024:
            bot.reply_to(message, "⚠️ El archivo es demasiado grande. El límite es 20 MB.")
            return
        
        # Download the file
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.reply_to(message, "⏳ Procesando tu archivo... Por favor espera.")
        
        output_file = None
        
        if conversion_type == 'pdf_a_docx':
            # Convert PDF to DOCX
            if not src.lower().endswith('.pdf'):
                bot.reply_to(message, "⚠️ Por favor envía un archivo PDF válido.")
                os.remove(src)
                return
            
            output_file = convert_to_docx(src)
            with open(output_file, 'rb') as docx_file:
                bot.send_document(chat_id, docx_file, caption="✅ ¡Conversión completada! PDF → DOCX")
        
        elif conversion_type == 'a_pdf':
            # Convert to PDF
            output_file = convert_to_pdf(src)
            with open(output_file, 'rb') as pdf_file:
                bot.send_document(chat_id, pdf_file, caption="✅ ¡Conversión completada! → PDF")
        
        # Clean up temporary files
        if output_file and os.path.exists(output_file):
            os.remove(output_file)
        if os.path.exists(src):
            os.remove(src)
        
        # Clear user state
        del user_states[chat_id]
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ocurrió un error: {str(e)}")
        # Clean up any remaining files
        try:
            if 'src' in locals() and os.path.exists(src):
                os.remove(src)
            if 'output_file' in locals() and output_file and os.path.exists(output_file):
                os.remove(output_file)
        except:
            pass
        # Clear user state
        if chat_id in user_states:
            del user_states[chat_id]

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.reply_to(message, "⚠️ Por favor usa /convert para iniciar una conversión o envía un documento.")

if __name__ == '__main__':
    print("🤖 Bot iniciado correctamente!")
    print(f"📊 Token: {TOKEN[:10]}... (oculto)")
    print("👋 Esperando mensajes...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"❌ Error en el bot: {e}")
