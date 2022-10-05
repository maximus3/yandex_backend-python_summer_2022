from datetime import date

from A import main as main_A
from B import main as main_B

from C import main as main_C
from C import str_to_date

from E import main as main_E

from E_right import main as main_E_right


data_A = [
    (('COVER', 'CLEAR'), ['correct', 'absent', 'present', 'absent', 'correct']),
    (('ABBA', 'AAAA'), ['correct', 'absent', 'absent', 'correct']),
    (('ABCBC', 'BBACA'), ['present', 'correct', 'present', 'present', 'absent'])
]

data_B = [
    ((2, [['ceo', '1'], ['co_founder', '1']], 3, ['arcady_volozh,ceo,6,100', 'elon_musk,ceo,5,0', 'ilya_segalovich,co_founder,6,10']), ['arcady_volozh', 'ilya_segalovich']),
    ((1, [['co_founder', '1']], 2, ['elon_musk,co_founder,6,200', 'ilya_segalovich,co_founder,6,100']), ['ilya_segalovich']),
    ((2, [['developer', '2'], ['hacker', '3']], 5, ['anonymous,hacker,6,0', 'bjarne_stroustrup,developer,6,1', 'julian_assange,hacker,5,100500', 'bill_gates,developer,3,1', 'guccifer,hacker,2,0']), ['anonymous', 'bill_gates', 'bjarne_stroustrup', 'guccifer', 'julian_assange']),
    ((2, [['plant', '2'], ['gardener', '1']], 5, ['demeter,gardener,4,12', 'acacia,plant,0,5', 'cactus,plant,0,1', 'ficus,plant,0,4', 'palm,plant,0,3']), ['cactus', 'demeter', 'palm']),
]

data_C = [
    ((
         [{"id": 1, "name": "Asus notebook","price": 1564,"date": "23.09.2021"},{"id": 2, "name": "Earpods", "price": 2200, "date": "10.01.2022"},{"id": 3, "name": "Keyboard", "price": 2500, "date": "05.06.2020"}, {"id": 4, "name": "Dell notebook","price": 2300,"date": "23.09.2021"}],
         {
             'NAME_CONTAINS': 'notebook',
             'PRICE_GREATER_THAN': '2000',
             'PRICE_LESS_THAN': '2400',
             'DATE_AFTER': '12.09.2021',
             'DATE_BEFORE': '02.01.2022',
         },
     ), '[{"id": 4, "name": "Dell notebook", "price": 2300, "date": "23.09.2021"}]'),
]

data_E = [
    ((')',), 1),
    (('(',), 1),

    (('((',), -1),
    (('()',), -1),
    ((')(',), -1),
    (('))',), -1),

    (('(((',), -1),
    (('(()',), 1),
    (('()(',), 3),
    (('())',), 2),
    ((')((',), -1),
    ((')()',), 1),
    (('))(',), -1),
    ((')))',), -1),

    (('((((',), -1),
    (('((()',), -1),
    (('(()(',), -1),
    (('(())',), -1),
    (('()((',), -1),
    (('()()',), -1),
    (('())(',), -1),
    (('()))',), -1),
    ((')(((',), -1),
    ((')(()',), -1),
    ((')()(',), -1),
    ((')())',), -1),
    (('))((',), -1),
    (('))()',), -1),
    ((')))(',), -1),
    (('))))',), -1),

    (('(((((',), -1),
    (('(((()',), -1),
    (('((()(',), -1),
    (('((())',), 1),
    (('(()((',), -1),
    (('(()()',), 1),
    (('(())(',), 5),
    (('(()))',), 3),
    (('()(((',), -1),
    (('()(()',), 3),
    (('()()(',), 5),
    (('()())',), 4),
    (('())((',), -1),
    (('())()',), 2),
    (('()))(',), -1),
    (('())))',), -1),
    ((')((((',), -1),
    ((')((()',), -1),
    ((')(()(',), -1),
    ((')(())',), 1),
    ((')()((',), -1),
    ((')()()',), 1),
    ((')())(',), -1),
    ((')()))',), -1),
    (('))(((',), -1),
    (('))(()',), -1),
    (('))()(',), -1),
    (('))())',), -1),
    ((')))((',), -1),
    ((')))()',), -1),
    (('))))(',), -1),
    ((')))))',), -1),

    (('(()()))',), 5),

    (('a + b = b + a',), -1),
    (('d + (a + (b + c) = (a + b) + c + d',), 5),
    (('(a((b + c) = ab + bc',), -1),
]


if __name__ == '__main__':
    data = data_E
    main = main_E
    for data_in, data_out in data:
        result = main(*data_in)
        right = main_E_right(*data_in)
        assert result == right, f'{data_in}\n{result} != {right}'
        # assert result == data_out, f'{data_in}\n{result} != {data_out}'
    print('All OK')
