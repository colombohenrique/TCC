
from django.urls import path
from .views import IndexView
from django.http import JsonResponse
from rest_framework import routers


def submit(request):

    perg1 = int(request.GET.get('perg1'))
    perg2 = int(request.GET.get('perg2'))
    perg3 = int(request.GET.get('perg3'))
    perg4 = int(request.GET.get('perg4'))
    perg5 = int(request.GET.get('perg5'))
    perg6 = int(request.GET.get('perg6'))
    perg7 = int(request.GET.get('perg7'))
    perg8 = int(request.GET.get('perg8'))
    perg9 = int(request.GET.get('perg9'))
    perg10 = int(request.GET.get('perg10'))
    perg11 = int(request.GET.get('perg11'))
    perg12 = int(request.GET.get('perg12'))
    perg13 = int(request.GET.get('perg13'))
    perg14 = int(request.GET.get('perg14'))
    perg15 = int(request.GET.get('perg15'))
    perg16 = int(request.GET.get('perg16'))
    perg17 = int(request.GET.get('perg17'))
    perg18 = int(request.GET.get('perg18'))

    def tipo(resultado):
        valor_desatento = perg1 + perg2 + perg3 + perg4 + \
            perg5 + perg6 + perg7 + perg8 + perg9

        valor_hipe_impulsivo = perg10 + perg11 + perg12 + \
            perg13 + perg14 + perg15 + perg16 + perg17 + perg18

        if valor_desatento >= 6:
            if valor_hipe_impulsivo >= 6:
                tipo = "Tipo Combinado"
            else:
                tipo = tipo = "Predominantemente Desatento"

        if valor_hipe_impulsivo >= 6:
            if valor_desatento >= 6:
                tipo = "Tipo Combinado"
            else:
                tipo = "Predominantemente Hiperativo/Impulsivo"

        if valor_desatento < 6 and valor_hipe_impulsivo < 6:
            tipo = "Sem predominância"

        if resultado >= 13.5:
            mostraTipo = "Muito Provável - " + tipo
        elif resultado >= 4.5 and resultado < 13.5:
            mostraTipo = "Provável - " + tipo  
        elif resultado < 4.5:
            mostraTipo = "Pouco Provável - " + tipo 
 
        return mostraTipo

    def func():

        valor_desatento = perg1 + perg2 + perg3 + perg4 + \
            perg5 + perg6 + perg7 + perg8 + perg9

        valor_hipe_impulsivo = perg10 + perg11 + perg12 + \
            perg13 + perg14 + perg15 + perg16 + perg17 + perg18

        import numpy as np
        import skfuzzy as fuzz
        from skfuzzy import control as ctrl

        desatento = ctrl.Antecedent(
            np.arange(0, 10, 1), 'desatento')

        hipe_impulsivo = ctrl.Antecedent(
            np.arange(0, 10, 1), 'hiperativo/impulsivo')

        diagnostico = ctrl.Consequent(np.arange(0, 19, 1), 'diagnostico')

        desatento.automf(
            names=['baixo', 'medio', 'alto'])
            
        hipe_impulsivo.automf(
            names=['baixo', 'medio', 'alto'])

        diagnostico.automf(
            names=['Pouco Provável', 'Provável', 'Muito Provável'])

        #desatento['baixo'] = fuzz.trimf(desatento.universe, [0, 0, 6])
        #desatento['medio'] = fuzz.trimf(desatento.universe, [0, 6, 9])
        #desatento['alto'] = fuzz.trimf(desatento.universe, [6, 9, 9])

        #hipe_impulsivo['baixo'] = fuzz.trimf(hipe_impulsivo.universe, [0, 0, 6])
        #hipe_impulsivo['medio'] = fuzz.trimf(hipe_impulsivo.universe, [0, 6, 9])
        #hipe_impulsivo['alto'] = fuzz.trimf(hipe_impulsivo.universe, [6, 9, 9])

        #diagnostico['Pouco Provável'] = fuzz.trimf(
        #    diagnostico.universe,[0, 0, 9])
        #diagnostico['Provável'] = fuzz.trimf(
        #    diagnostico.universe, [0, 9, 19])
        #diagnostico['Muito Provável'] = fuzz.trimf(
        #    diagnostico.universe, [9, 19, 19])


        
        rule1 = ctrl.Rule(
            desatento['alto'] & hipe_impulsivo['alto'], diagnostico['Muito Provável'])
        rule2 = ctrl.Rule(
            desatento['alto'] & hipe_impulsivo['medio'], diagnostico['Muito Provável'])
        rule3 = ctrl.Rule(
            desatento['medio'] & hipe_impulsivo['alto'], diagnostico['Muito Provável'])
        rule4 = ctrl.Rule(
            desatento['medio'] & hipe_impulsivo['medio'], diagnostico['Pouco Provável'])
        rule5 = ctrl.Rule(
            desatento['baixo'] & hipe_impulsivo['medio'], diagnostico['Pouco Provável'])
        rule6 = ctrl.Rule(
            desatento['medio'] & hipe_impulsivo['baixo'], diagnostico['Pouco Provável'])
        rule7 = ctrl.Rule(
            desatento['alto'] & hipe_impulsivo['baixo'], diagnostico['Provável'])
        rule8 = ctrl.Rule(
            desatento['baixo'] & hipe_impulsivo['alto'], diagnostico['Provável'])
        rule9 = ctrl.Rule(
            desatento['baixo'] & hipe_impulsivo['baixo'], diagnostico['Pouco Provável'])

        diagnostico_ctrl = ctrl.ControlSystem(
            [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
        diagnostico_simulator = ctrl.ControlSystemSimulation(diagnostico_ctrl)

        diagnostico_simulator.input['desatento'] = valor_desatento
        diagnostico_simulator.input['hiperativo/impulsivo'] = valor_hipe_impulsivo

        diagnostico_simulator.compute()

        valor_diagnostico = diagnostico_simulator.output['diagnostico']

        print(valor_desatento)
        print(valor_hipe_impulsivo)
        print(valor_diagnostico)

        if valor_desatento == 9 and valor_hipe_impulsivo == 9:
            valor_diagnostico = 17
        
        if valor_desatento == 0 and valor_hipe_impulsivo == 0:
            valor_diagnostico = 0

        return valor_diagnostico

    varResult = func()
    varTipo = tipo(varResult)

    return JsonResponse({
        "resultado": varTipo,
        "grafico": varResult,
        "texto": "Obs: Diagnóstico feito com base no Manual DSM IV e com as regras definidas no sistema Fuzzy, não substituí diagnóstico de um profissional. Para diagnóstico válido, procurar um especialista."
    })


urlpatterns = [
    # path('endereco/', MinhaView.asview(), name='nome da url'),
    path('', IndexView.as_view(), name='inicio'),
    path('submit', submit, name='submit'),
]
