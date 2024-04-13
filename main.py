from flask import Flask, render_template
import matplotlib.pyplot as plt
import mysql.connector

app = Flask(__name__)


# Функция для получения данных из базы данных
def get_data_from_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="rps"
    )
    cursor = conn.cursor()

    # Получаем координаты узлов
    cursor.execute("SELECT id, x, y FROM nodes")
    nodes = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}

    # Получаем тройки узловых точек элементов
    cursor.execute("SELECT id, n1, n2, n3 FROM elements")
    elements = [(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]

    conn.close()

    return nodes, elements


# Функция для нахождения центра масс треугольника
def calculate_triangle_center(node1, node2, node3):
    x = (node1[0] + node2[0] + node3[0]) / 3
    y = (node1[1] + node2[1] + node3[1]) / 3
    return x, y


# Функция для создания графика
def create_plot(nodes, elements):
    plt.figure(figsize=(8, 6))
    for element in elements:
        node1 = nodes[element[1]]
        node2 = nodes[element[2]]
        node3 = nodes[element[3]]
        center = calculate_triangle_center(node1, node2, node3)
        plt.plot(center[0], center[1], 'ro')  # Рисуем центр масс треугольника

        # Рисуем линии треугольника
        plt.plot([node1[0], node2[0]], [node1[1], node2[1]], 'b-')
        plt.plot([node2[0], node3[0]], [node2[1], node3[1]], 'b-')
        plt.plot([node3[0], node1[0]], [node3[1], node1[1]], 'b-')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Сетка треугольных элементов')
    plt.grid(True)
    plt.axis('equal')
    plt.savefig('static/plot.png')  # Сохраняем график как изображение


@app.route('/')
def index():
    nodes, elements = get_data_from_db()
    create_plot(nodes, elements)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
