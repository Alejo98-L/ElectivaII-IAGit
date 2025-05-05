import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense 
from tensorflow.keras.utils import to_categorical 
from PIL import Image
import os
import venv

# Ruta a la carpeta que contiene las imágenes
carpeta_numeros = os.path.join(os.path.dirname(__file__), 'Numeros')

# Lista de archivos de imagen en la carpeta
imagenes = []
etiquetas = []

tamaño_imagen = (28, 28)

for nombre_archivo in os.listdir(carpeta_numeros):
    if nombre_archivo.endswith('.png'):
        ruta_completa = os.path.join(carpeta_numeros, nombre_archivo)
        imagen = Image.open(ruta_completa).convert('L')  # 'L' convierte a escala de grises si es necesario
        imagen = imagen.resize(tamaño_imagen)
        imagenes.append(np.array(imagen))

        # Por ejemplo: la etiqueta podría estar en el nombre del archivo (como '1_3.png' -> etiqueta 1)
        etiqueta = int(nombre_archivo[0])  # Asumiendo que la etiqueta es el primer carácter
        etiquetas.append(etiqueta)

# Ahora puedes dividir en entrenamiento y prueba
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(imagenes, etiquetas, test_size=0.25, random_state=42)

# 2. Preprocesamiento
x_train = np.array(x_train) / 255.0
x_test = np.array(x_test) / 255.0

# Añadir canal (imágenes grises)
x_train = np.expand_dims(x_train, -1)  # (60000, 28, 28, 1)
x_test = np.expand_dims(x_test, -1)

# One-hot encoding de las etiquetas
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)

# 3. Visualizar algunas imágenes
print("Mostrando ejemplos del dataset...")
fig, axes = plt.subplots(1, 5, figsize=(10, 3))
for i in range(5):
    axes[i].imshow(x_train[i].squeeze(), cmap='gray')
    axes[i].axis('off')
    axes[i].set_title(f"Etiqueta: {y_train[i]}")
plt.show()

# 4. Crear el modelo CNN
print("Creando el modelo CNN...")
model = Sequential([
    Conv2D(28, (3,3), activation='relu', input_shape=(28,28,1)),
    MaxPooling2D((2,2)),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D((2,2)),
    Flatten(),# Aplanamos la salida de las capas convolucionales
    Dense(128, activation='relu'), # Ajustar la capa densa con un número de neuronas adecuado
    Dense(10, activation='softmax')
])

# Compilar el modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 5. Entrenar el modelo
print("Entrenando el modelo...")
history = model.fit(x_train, y_train_cat, epochs=10, validation_data=(x_test, y_test_cat))

# 6. Graficar resultados
print("Graficando resultados...")

fig2, ax2 = plt.subplots(1, 2, figsize=(12,4))

# Accuracy
ax2[0].plot(history.history['accuracy'], label='Entrenamiento')
ax2[0].plot(history.history['val_accuracy'], label='Validación')
ax2[0].set_title('Precisión (Accuracy)')
ax2[0].legend()

# Loss
ax2[1].plot(history.history['loss'], label='Entrenamiento')
ax2[1].plot(history.history['val_loss'], label='Validación')
ax2[1].set_title('Pérdida (Loss)')
ax2[1].legend()

plt.show()

# 7. Evaluar modelo final
print("Evaluando el modelo en el conjunto de prueba...")
loss, acc = model.evaluate(x_test, y_test_cat, verbose=0)
print(f"\nPrecisión en Test: {acc:.4f}")
print(f"Pérdida en Test: {loss:.4f}")
#8. Guardar el modelo
model.save('modelo_cnn_def.keras')