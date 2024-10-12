import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Flatten, Dense, Dropout
import matplotlib.pyplot as plt 

data = pd.read_csv('data_clean.csv')

print(data.head())

features = [
    'Score', 'Pick %', 'Dmg/Round', 'KDA', 
    'Attacker Win %', 'Attacker KDA', 
    'Defender Win %', 'Defender KDA',
    'A Pick %', 'A Defuse %', 'B Pick %', 
    'B Defuse %', 'C Pick %', 'C Defuse %'
]

data['Winner'] = (data['Win %'] > 0.5).astype(int) 

X = data[features].values
y = data['Winner'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = X_train.reshape((X_train.shape[0], 14, 1)) 
X_test = X_test.reshape((X_test.shape[0], 14, 1))   

model = Sequential()
model.add(Conv1D(filters=32, kernel_size=2, activation='relu', input_shape=(14, 1)))  # input_shape = (14, 1)
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(16, activation='relu'))
model.add(Dense(1, activation='sigmoid')) 

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=20, batch_size=16, validation_data=(X_test, y_test))

loss, accuracy = model.evaluate(X_test, y_test)
# print(f'Test Accuracy: {accuracy:.2f}')
model.save('cnn_model.h5')

est_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test accuracy: {test_accuracy:.4f}')

plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend()
plt.show()

plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()
