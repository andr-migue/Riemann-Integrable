import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import TextBox, Button
import sympy as sp

# CONFIGURACIÓN INICIAL
x = sp.symbols('x')
function = sp.simplify("sin(x) + 1")
fx = sp.lambdify(x, function, "numpy")
a, b = 0, 6
partitions = 50

# CREACIÓN DE LA FIGURA
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
xVals = np.linspace(a, b, 1000)
yVals = fx(xVals)
line, = ax.plot(xVals, yVals, label=f"f(x) = {function}", color="blue")

# CUADRÍCULA DE COORDENADAS
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)  # Cuadrícula apenas visible

# LÍNEAS DE REFERENCIA PARA LOS EJES X E Y
ax.axhline(0, color="black", linewidth=1.5)  # Eje X
ax.axvline(0, color="black", linewidth=1.5)  # Eje Y

upperLine, = ax.plot([], [], label="Suma superior", color="red", linestyle="--")
lowerLine, = ax.plot([], [], label="Suma inferior", color="green", linestyle="--")
rects = []
text = ax.text(0.02, 0.95, "", transform=ax.transAxes, ha="left", va="top", fontsize=10, bbox=dict(facecolor="white", alpha=0.8))
ax.legend()

# Inicializar la variable de animación
ani = None

# FUNCIÓN PARA CALCULAR SUMAS
def CalculateSums(n):
    xPartition = np.linspace(a, b, n + 1)
    upperSum, lowerSum = 0, 0
    upperX, upperY, lowerX, lowerY = [], [], [], []
    bars = []
    width = (b - a) / n

    for i in range(n):
        left = xPartition[i]
        right = xPartition[i + 1]
        values = fx(np.linspace(left, right, 100))
        Mi = np.max(values)
        mi = np.min(values)

        upperSum += Mi * (right - left)
        lowerSum += mi * (right - left)

        upperX.extend([left, right])
        upperY.extend([Mi, Mi])
        lowerX.extend([left, right])
        lowerY.extend([mi, mi])

        bars.append((left, 0, width, Mi, "red"))
        bars.append((left, 0, width, mi, "limegreen"))

    return upperX, upperY, lowerX, lowerY, upperSum, lowerSum, bars

# FUNCIÓN PARA ACTUALIZAR LA ANIMACIÓN
def Update(n):
    global rects
    upperX, upperY, lowerX, lowerY, upperSum, lowerSum, bars = CalculateSums(n + 1)
    upperLine.set_data(upperX, upperY)
    lowerLine.set_data(lowerX, lowerY)
    text.set_text(f"Partición: {n + 1} \n Suma sup: {upperSum:.4f} \n Suma inf: {lowerSum:.4f} \n Diferencia: {upperSum - lowerSum:.4f}")

    for rect in rects:
        rect.remove()
    rects = []

    for x, y, w, h, color in bars:
        rect = ax.add_patch(plt.Rectangle((x, 0), w, h, color=color, alpha=0.5))
        rects.append(rect)
    
    return [upperLine, lowerLine, text] + rects

# FUNCIÓN PARA INICIAR ANIMACIÓN
def StartAnimation(event):
    global ani
    ani = FuncAnimation(fig, Update, frames=partitions, blit=False, interval=500, repeat=False)
    plt.draw()

# FUNCIÓN PARA DETENER LA ANIMACIÓN
def StopAnimation(event):
    global ani
    if ani is not None:  # Verificar si la animación está inicializada
        ani.event_source.stop()
        plt.draw()

# FUNCIÓN PARA APLICAR CAMBIOS EN TIEMPO REAL
def ApplyChanges(event):
    global function, fx, a, b, partitions

    try:
        function = sp.sympify(textBox.text)
        fx = sp.lambdify(x, function, "numpy")
    except Exception as e:
        print(f"Error en función: {e}")
        return

    try:
        a = float(textBoxA.text)
        b = float(textBoxB.text)
        if a >= b:
            raise ValueError("El valor de 'a' debe ser menor que 'b'.")
    except ValueError as e:
        print(f"Error en intervalo: {e}")
        return

    try:
        partitions = int(textBoxN.text)
        if partitions < 1:
            raise ValueError("El número de particiones debe ser mayor que 0.")
    except ValueError as e:
        print(f"Error en particiones: {e}")
        return

    # Actualizar solo los elementos que cambian
    xVals = np.linspace(a, b, 1000)
    yVals = fx(xVals)
    line.set_data(xVals, yVals)
    line.set_label(f"f(x) = {function}")
    ax.relim()
    ax.autoscale_view()
    ax.legend()
    plt.draw()

# CREACIÓN DE ELEMENTOS DE INTERFAZ
axBoxFunc = plt.axes([0.1, 0.25, 0.3, 0.05])
textBox = TextBox(axBoxFunc, "Función: ", initial="sin(x) + 1")
textBox.on_submit(ApplyChanges)

axBoxA = plt.axes([0.1, 0.18, 0.1, 0.05])
textBoxA = TextBox(axBoxA, "a: ", initial="0")
textBoxA.on_submit(ApplyChanges)

axBoxB = plt.axes([0.25, 0.18, 0.1, 0.05])
textBoxB = TextBox(axBoxB, "b: ", initial="6")
textBoxB.on_submit(ApplyChanges)

axBoxN = plt.axes([0.1, 0.11, 0.3, 0.05])
textBoxN = TextBox(axBoxN, "Particiones: ", initial="50")
textBoxN.on_submit(ApplyChanges)

axStart = plt.axes([0.6, 0.25, 0.2, 0.075])
buttonStart = Button(axStart, "Iniciar Animación")
buttonStart.on_clicked(StartAnimation)

axStop = plt.axes([0.6, 0.15, 0.2, 0.075])
buttonStop = Button(axStop, "Detener Animación")
buttonStop.on_clicked(StopAnimation)

plt.show()