import tensorflow as tf
import numpy as np

# Palabra a aprender
word = "hola"

# Crear el diccionario de caracteres
chars = sorted(set(word))
char_to_idx = {c: i for i, c in enumerate(chars)}
idx_to_char = {i: c for c, i in char_to_idx.items()}
vocab_size = len(chars)

# Función para convertir a one-hot
def to_one_hot(idx, vocab_size):
    one_hot = np.zeros(vocab_size)
    one_hot[idx] = 1.0
    return one_hot

# Preparar datos de entrada (X) y salida (y)
X = []
y = []

for i in range(len(word) - 1):
    seq = word[:i + 1]
    target = word[i + 1]
    
    x_seq = [to_one_hot(char_to_idx[c], vocab_size) for c in seq]
    X.append(x_seq)
    y.append(char_to_idx[target])

# Rellenar las secuencias a la misma longitud
max_len = max(len(seq) for seq in X)
X_padded = []

for seq in X:
    # Pad con ceros
    while len(seq) < max_len:
        seq.insert(0, np.zeros(vocab_size))
    X_padded.append(seq)

# Convertir a arrays numpy
X_padded = np.array(X_padded)
y = np.array(y)

# Crear el modelo RNN
model = tf.keras.Sequential([
    tf.keras.layers.SimpleRNN(50, input_shape=(max_len, vocab_size), activation='relu'),
    tf.keras.layers.Dense(vocab_size, activation='softmax')
])

# Compilar el modelo
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit(X_padded, y, epochs=500, verbose=0)

# Función para predecir la siguiente letra
def predict_next_char(model, input_seq):
    encoded = [to_one_hot(char_to_idx[c], vocab_size) for c in input_seq]
    while len(encoded) < max_len:
        encoded.insert(0, np.zeros(vocab_size))
    encoded = np.array([encoded])
    pred = model.predict(encoded, verbose=0)
    predicted_idx = np.argmax(pred)
    return idx_to_char[predicted_idx]

# Probar predicciones
test_inputs = ["h", "ho", "hol"]
for seq in test_inputs:
    predicted = predict_next_char(model, seq)
    print(f"'{seq}' -> '{predicted}'")
