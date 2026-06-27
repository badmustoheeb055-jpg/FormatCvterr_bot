import os
import time
import telebot as tb
from mensajes import *
from pdf_converter import convert_to_docx, convert_to_pdf, convertir_ppt_to_pdf_linux
#botones inline

#El comienzo
bot = tb.TeleBot('TU_TOKEN_AQUI')

@bot.message_handler(commands = ['start'])
def enviar_mensaje(message):
    bot.reply_to(message,texto_bienvenida)
    bot.reply_to(message,texto_convertir)

@bot.message_handler(commands = ['convert'])
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
        bot.send_message(call.message.chat.id, "Envía el archivo PDF que deseas convertir a DOCX.")
        # Guardar estado del usuario
        # context.user_data['conversion_type'] = 'pdf_a_docx' # Si usas pyTelegramBotAPI, puedes usar un dict global
    elif call.data == "a_pdf":
        bot.answer_callback_query(call.id, "Opción seleccionada: Convertir a PDF")
        bot.send_message(call.message.chat.id, "Envía el archivo que deseas convertir a PDF.")
        # Guardar estado del usuario

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    # Verificar estado del usuario para saber qué conversión hacer
    # Ejemplo: if user_state == 'pdf_a_docx': ...
    # Por simplicidad, asumimos que el usuario eligió PDF a DOCX
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Aquí se llama a la función de conversión
        # output_file = convert_to_docx(src)
        # bot.send_document(message.chat.id, open(output_file, 'rb'))
        
        # Limpiar archivos temporales
        os.remove(src)
        # os.remove(output_file)
    except Exception as e:
        bot.reply_to(message, f"Ocurrió un error: {e}")

bot.polling()
