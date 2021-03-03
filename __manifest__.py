# -*- coding: utf-8 -*-
{
    'name': 'Sevo Studio Force 500',
    'summary': 'Crea y organiza presupuestos de Force 500',
    'description': """
        Módulo diseñado por Sevo Europe SL para:
        - Crear presupuestos personalizados en PDF
        - Organizar los presupuestos y proyectos
        - Sincronizar los proyectos con los empleados
    """,
    'author': "Sevo Europe SL",
    'website': "http://www.sevoeurope.com",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base', 'sale', 'mail', 'crm', 'sevostudio'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/force_view.xml',
        'views/agent_view.xml',
        'views/cylinder_view.xml',
        'views/room_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ]
}
