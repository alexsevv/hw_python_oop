from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """ Информационное сообщение о тренировке. """
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    """
    Преобразуем экземляр класса данных в словарь
    и округляем при выводе до тысячных долей с помощью
    format specifier (.3f)
    """

    def get_message(self) -> None:
        return self.MESSAGE.format(*asdict(self).values())


class Training:
    """ Базовый класс тренировки. """
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINUT_IN_HOUR: int = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """ Получаем дистанцию в км. action * LEN_STEP / M_IN_KM """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """
        Получить среднюю скорость движения.
        преодоленная_дистанция_за_тренировку / время_тренировки
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """ Получить количество затраченных калорий. """
        raise NotImplementedError(
            'Определите get_spent_calories в %s.' %
            (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """ Вернем информационное сообщение о выполненной тренировке. """
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """ Тренировка: бег. """
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """
        Получим количество затраченных калорий.
        (18 * средняя_скорость - 20) * вес_спортсмена / M_IN_KM
        * время_тренировки_в_минутах
        """
        return ((self.COEFF_CALORIE_1
                * self.get_mean_speed()
                - self.COEFF_CALORIE_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MINUT_IN_HOUR)


class SportsWalking(Training):
    """ Тренировка: спортивная ходьба. """
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: int = 2
    COEFF_CALORIE_3: float = 0.029

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """
        Получим количество затраченных калорий.
        (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес)
        * время_тренировки_в_минутах
        """
        return ((self.COEFF_CALORIE_1
                * self.weight
                + (self.get_mean_speed()
                 ** self.COEFF_CALORIE_2
                 // self.height)
                * self.COEFF_CALORIE_3
                * self.weight)
                * self.duration
                * self.MINUT_IN_HOUR)


class Swimming(Training):
    """ Тренировка: плавание. """
    LEN_STEP = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """
        длина_бассейна * count_pool / M_IN_KM / время_тренировки
        """
        return (self.lenght_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """(средняя_скорость + 1.1) * 2 * вес """
        return ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """ Прочитаем данные полученные от датчиков. """
    parameters_workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type in parameters_workout:
        return parameters_workout[workout_type](*data)

    raise ValueError(f"Тренировка {workout_type} не найдена")


def main(training: Training) -> None:
    """ Главная функция. """
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
