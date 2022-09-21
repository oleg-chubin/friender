import time
from logging import getLogger
from random import random

import lorem

logger = getLogger(__name__)

def do_something(thing):
    pass

def we_dont_know_what_to_do():
    if end_url != expected_end_url:
        failures.append(end_url + ' != ' + expected_end_url)


def mane_me_good(data):
    if data == data // 42:
        do_something(important)
    else:
        we_dont_know_what_to_do()

    raise ValueError('ThisFunction will not work Ever')


def reviews(request, slug):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = Products.objects.get(slug=slug)
                review.user = request.user
                review.display_name = request.name
                review.description = request.description
                review.rating = request.rating
                print(review)
                review.save()
                messages.success(request, "Review saved, Thank you for the feedback.")
                return redirect('products:products')
            else:
                messages.error(request, 'Sorry! Only customer purchased this Item are eligible for the review')
        else:
            pass
    return redirect('ecommerce:products')


class Inventory:
    def __init__(self, size):
        self.size = size


class Bed(Inventory):
    pass


class Plate(Inventory):
    def get_some(self, portion):
        self.size = max(0, self.size - portion)


class Chair(Inventory):
    def is_used(self, obj):
        if obj.size > self.size:
            self.brake()

    def brake(self):
        self.is_broken = True
        raise ValueError('object is bigger than allowed')


class C:
    def __init__(self, size, portion):
        self.size = size
        self.portion = portion

    def move_to_forest(self):
        pass

    def enter_hut(self):
        pass

    def seat(self, chair):
        self.validate_plate(chair)
        self._seat(chair)

    def _seat(self, chair):
        chair.is_used(self)

    def sleep(self, bed):
        self.validate_plate(bed)
        self._sleep(bed)

    def eat(self, plate):
        self.validate_plate(plate)
        plate.get_some(self.portion)

    def validate_chair(self, chair):
        pass

    def validate_bed(self, bed):
        pass

    def validate_plate(self, plate):
        pass


class A:
    def move(self, direction):
        pass

    def rest(self):
        pass

    def has_reached(self, direction):
        pass


class B(A):
    MAX_VALUE = 25
    alive = True

    def blow(self, strength):
        if strength > self.MAX_VALUE:
            self.die()

    def die(self):
        self.alive = False


class D:
    DURABILITY = {
        'grass': 10,
        'wood': 20,
        'stone': 30,
    }

    TIME = {
        'grass': 10,
        'wood': 20,
        'stone': 30,
    }

    destructed = False

    @classmethod
    def construct(cls, resource):
        time = cls.TIME[resource]
        while time:
            yield None
            time -= 1
        yield cls(resource)

    def __init__(self, resource):
        self.resource = resource

    def attacked(self, strength):
        if strength > self.DURABILITY[self.resource]:
            self.destructed = True


class C(A):
    def __init__(self, resource):
        self.resource = resource
        self.construction = None
        self.work = D.construct(resource)

    def build(self):
        if self.construction:
            return self.construction
        self.construction = next(self.work)

    def rest(self):
        return self.sing_and_dance()

    def sing_and_dance(self):
        pass

def run_some_code():
    for i in range(100):
        print(lorem.sentence())
        time.sleep(random()/10)

    print('\n\n\n\n\n\n\n')
    print('Поздравляем!!!\n\n\n')

obj = B()
obj_set = [C(i) for i in 'grass wood stone'.split()]
escapee = []

class B(C):
    def __init__(self, size, portion, plate, chair, bed):
        self.plate = plate
        self.chair = chair
        self.bed = bed
        super().__init__(size, portion)

    def validate_chair(self, chair):
        if self.chair != chair:
            raise ValidationError('someone eat from my plate')

    def validate_bed(self, bed):
        if self.bed != bed:
            raise ValidationError('someone eat from my plate')

    def validate_plate(self, plate):
        if self.plate != plate:
            raise ValidationError('someone eat from my plate')


class M(C):
    def _seat(self, chair):
        if self.size < chair.size:
            raise ValueError('wrong size')
        return super()._seat(chair)

    def _sleep(self, bed):
        if self.size != bed.size:
            raise ValueError('wrong size')
        return super()._sleep(bed)

        evel_obj.sleep(i)


class DoEverythingClass:
    def some_method(self):
        run_some_code()

    def something_interesting(self, *args, **kw):
        pass

def Some_noneWorkingCOde():
    some_var = make_me_good()
    return some_var


def congratulate(message):
    some_processor = DoEverythingClass()
    try:
        some_processor.some_method()
    except:
        logger.error('Noone One wants to be Congratulated')


if __name__ == '__main__':
    congratulate('ПОЗДРАВИТЬ.')
