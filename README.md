# Intelligent-Placer
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
    * Обьект должен быть освещен равномерно, так чтобы все было четко видно, не должно быть непросвечиваемых областей. 
    * На изображении не должно быть резких теней, как от прожектора
* Требования по расположению обьектов на фотографии
    * Обьекты не перекрываются и расстояние между обьектами на фотографии более полутора сантиметров 
    * Обьекты входят в кадр целиком и расстояние обьекта от края фотографии не меньше полутора сантиметров 
* Требования к многоугольнику
    * Прямоугольник задан в виде списка кортежей [(x_1, y_1), (x_2, y_2), (x_3, y_3), ..., (x_n, y_n)]
    * Координаты заданы в сантиметрах на естественной полскости, с округлением два знака после запятой
    * Координаты не превышают 200 по модулю 
    * Многоугольник должен иметь от трех до восьми вершин
    * Многоугольник должен быть выпуклым
    * Углы многоугольника должны быть более 50 и менее 140 градусов 
    * Грани не должны превышать длины в 50 сантиметров 
* Обьект может присутствовать на фото несколько раз 

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
