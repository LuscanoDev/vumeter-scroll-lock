# VU Meter Scroll lock
um medidor de som que funciona pelo led do scroll lock.

# instalação
> para rodar esse script, você **PRECISA** ter linux. talvez deve ter alguma forma de fazer isso funcionar no windows, mas como eu não tenho nenhum pc windows para testar isso, vai ficar sem por enquanto. seja livre para fazer um pull request caso descubra como fazer.

para rodar o script, você só precisa instalar as blibiotecas necessárias com `pip install -r requirements.txt` e rodar o script com `python main.py`.

# como isso funciona?
o script liga e desliga o led do scroll lock várias vezes por segundo. como não dá para ajustar o brilho dos leds do teclado com precisão, eu tive que usar esse método de ligar e desligar rápido com um delay específico. isso cria a ilusão de um brilho mais fraco, e assim consigo sincronizar o led com o som usando essa técnica.
