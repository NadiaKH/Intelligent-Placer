# Intelligent-Placer
## Описание данных
Прежде, чем описывать задачу, я хочу описать файл с собранными данными

Ссылка на данные https://drive.google.com/drive/folders/1e3rQsB-8N364o7oq8eVdH8vPkYrc0U3t?usp=sharing

В файле data содержатся
* IMGS - входные фотографии 
* figures_coordinates.json - многоугольники, заданные покоординатно 
* polygons_vizualized - графики многоугольников
* can_be_plased.csv - таблица, со столбцами 
    * **IMG** - номер изображения 
    * **fig** - номер фигуры 
    * **can_be_placed** - колонка типа bool могут ли предметы, находящиеся на изображении, поместиться в фигуру    

Репрезентативные примеры находятся в файле Representative.

Их описание:

*Замечание: номера фигур брать из файла can_be_placed.csv*

* 07, 14, 11, 23, 25 - особенны тем, что для их укладки в фигуру надо использовать особенности стыковки предметов 
* 33, 34, 35, 36 - особенны тем, что там много предметов
* 40 - особенна тем, что предметы надо плотно уложить 
## Требования

**Входные данные:** на вход получает фотографию, удовлетворяющую требованиям ниже и многоугольник, представленный списком с координатами вершин на естественной плоскости. Список координат дан в сантиметрах с округлением 2 знака после запятой: [(x_1, y_1), (x_2, y_2), (x_3, y_3), ..., (x_n, y_n)]. 

**Выходные данные:** на выход возвращает True - в случае, если алгоритму удалось разместить предметы в многоугольнике, False - если нет. 

* Фотометрические требования:
    * Разрешение по длине и ширине не менее 600 px
    * Высота съемки от 30 до 60 сантиметров над поверхностью
    * Изображение не должно быть размыто толщина границы не более 7px, то есть камера должна быть сфокусирована на фотографируемых обьектах.
    * Наклон камеры относительно вертикали не более 7 градусов
    * Не допускается черно белых снимков 
* Требования к освещению
    * Объект должен быть освещен равномерно, так чтобы все было четко видно, не должно быть непросвечиваемых областей. 
    * На изображении не должно быть резких теней, как от прожектора
* Требования по расположению обьектов на фотографии
    * Объекты не перекрываются и расстояние между обьектами на фотографии более полутора сантиметров 
    * Расстояние от границ изображений для всех обьектов должно быть более полутора сантиметров
    * Объекты входят в кадр целиком
    * Объекты входят в кадр целиком и расстояние обьекта от края фотографии не меньше полутора сантиметров 
* Требования к многоугольнику
    * Прямоугольник задан в виде списка кортежей [(x_1, y_1), (x_2, y_2), (x_3, y_3), ..., (x_n, y_n)]
    * Координаты заданы в сантиметрах на естественной полскости, с округлением два знака после запятой
    * Координаты не превышают 200 по модулю 
    * Многоугольник должен иметь от трех до восьми вершин
    * Многоугольник должен быть выпуклым
    * Углы многоугольника должны быть более 50 и менее 140 градусов 
    * Грани не должны превышать длины в 50 сантиметров 
* Объект может присутствовать на фото несколько раз (Этот пункт связан с автогенерацией тестов, когда на одну фотографию может быть помещено несколько копий объекта, в моём датасете таких приметов нет)

## Фото обьектов 
<table align="center">
            <td><img src="https://github.com/NadiaKH/Intelligent-Placer/blob/develop/%D0%A4%D0%BE%D1%82%D0%BE_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D0%96%D1%83%D0%BA.jpg" width="180" height="320"></td>
            <td><img src="https://github.com/NadiaKH/Intelligent-Placer/blob/develop/%D0%A4%D0%BE%D1%82%D0%BE_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D0%9A%D0%B0%D0%BC%D0%B5%D0%BD%D1%8C.jpg" width="180" height="320"></td>
            <td><img src="https://github.com/NadiaKH/Intelligent-Placer/blob/develop/%D0%A4%D0%BE%D1%82%D0%BE_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D0%9A%D0%B0%D1%80%D0%B0%D0%BD%D0%B4%D0%B0%D1%88.jpg" width="180" height="320"></td>
            <td><img src="https://github.com/NadiaKH/Intelligent-Placer/blob/develop/%D0%A4%D0%BE%D1%82%D0%BE_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D0%9A%D1%80%D0%B0%D0%B1%D0%B8%D0%BA.jpg" width="180" height="320"></td>
            
  </table>

<table align="center">
            <td><img src="https://github.com/NadiaKH/Intelligent-Placer/blob/develop/%D0%A4%D0%BE%D1%82%D0%BE_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D0%9E%D1%81%D0%BA%D0%BE%D0%BB%D0%BE%D0%BA.jpg" width="180" height="320"></td>
            <td><img src="https://github.com/NadiaKH/Intelligent-Placer/blob/develop/%D0%A4%D0%BE%D1%82%D0%BE_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D0%9F%D1%83%D0%B3%D0%BE%D0%B2%D0%B8%D1%86%D0%B0.jpg" width="180" height="320"></td>
            <td><img src="https://github.com/NadiaKH/Intelligent-Placer/blob/develop/%D0%A4%D0%BE%D1%82%D0%BE_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D0%A0%D1%83%D1%87%D0%BA%D0%B0.jpg" width="180" height="320"></td>
            <td><img src="https://github.com/NadiaKH/Intelligent-Placer/blob/develop/%D0%A4%D0%BE%D1%82%D0%BE_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D0%A1%D0%B5%D1%80%D0%B4%D0%B5%D1%87%D0%BA%D0%BE.jpg" width="180" height="320"></td>
            
  </table>
  
 <table align="center">
            <td><img src="https://github.com/NadiaKH/Intelligent-Placer/blob/develop/%D0%A4%D0%BE%D1%82%D0%BE_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D0%A2%D0%BE%D1%87%D0%B8%D0%BB%D0%BA%D0%B0.jpg" width="180" height="320"></td>
            <td><img src="https://github.com/NadiaKH/Intelligent-Placer/blob/develop/%D0%A4%D0%BE%D1%82%D0%BE_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D0%A2%D1%80%D0%B8%D0%BB%D0%B8%D1%81%D1%82%D0%BD%D0%B8%D0%BA.jpg" width="180" height="320"></td>
            <td><img src="https://github.com/NadiaKH/Intelligent-Placer/blob/develop/%D0%A4%D0%BE%D1%82%D0%BE_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D0%A4%D0%BE%D0%BD.jpg" width="180" height="320"></td>
            
  </table>
