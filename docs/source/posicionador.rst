Posicionador
=================
O posicionador linear é responsável por mover a antena para realizar a varredura.
Foi desenvolvido um driver para controlar este posicionador pelo computado.

Driver Posicionador
-----------------------

.. class:: positioner

    .. method:: __init__()
    No momento não faz nada além de iniciar o objeto

    .. method:: conenct(porta, b = 9600)

        :param porta: Porta serial em que o posicionador está conectado
        :param b: Baudrate da conexão serial. Alterando este parâmetro implicará reprogramar o posicionador para o novo valor também.

    .. method:: small_step_foward()

        Posicionador realiza um pequeno paço para frente.

    .. method:: big_step_foward()

        Posicionador realiza um grande paço para frente.

    .. method:: small_step_back()

        Posicionador realiza um pequeno paço para trás.

    .. method:: big_step_back()

        Posicionador realiza um grande passo para trás.

    .. method:: disconnect()
        
        Encerra a conexão serial com o posicionador.

.. note::
    O tamanho dos paços é definido pelo código do posicionador, sendo necessário alterar a programação deste e reprograma-lo para atualizações.