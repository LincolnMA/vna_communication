API VNA 
====

.. class:: Nvna

    .. method:: __init__( version = 3, baudrate = _default_baudrate, port_name = None)

        :param version:
            Versão do dispositivo usado, a versão 3 é a única utilizada geralmente.

        :param baudrate:
            Baudrate da conexão UART. Valores até 2000000 foram testados.
        
        :param port_name:
            Porta serial conectada ao dispositivo.

    .. method:: measure(start_f,end_f,n_points,nmpp)

        :param start_f:
            Frequência de início do estímulo.
        :param end_f:
            Frequência final do estímulo.
        :param n_points:
            Número de pontos de frequência medidos no estímulo.
        :param nmpp:
            Quantidade de medições por ponto. 

    .. method:: extract_S11()

        :return: Lista com frequências, parte Real e parte imaginária do S11.

        :rtype: list[list[int], list[int], list[int}]

        .. note::

            Deve-se fazer a calibração antes de chamar esse método.

    .. method:: calibration(start_f,end_f,n_points,nmpp)
        
        :param start_f:
            Frequência de início do estímulo.
        :param end_f:
            Frequência final do estímulo.
        :param n_points:
            Número de pontos de frequência medidos no estímulo.
        :param nmpp:
            Quantidade de medições por ponto. 


    .. method:: calibrate_S11()

        Realiza cálculos de correção de S11. Após a chamada desse método S11 calibrado pode ser extraído por outros métodos.     

    .. method:: load_calib(path)

        :param path: Caminho para o diretório onde está o arquivo de calibração.

    .. method:: save_calib(path)

        :param path:  

        Salva arquivo de calibração em diretório *path* 
