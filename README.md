# Iposim Automator

Este programa automatiza as simulações de perdas em semicondutores realizadas através do Iposim, ferramenta de simulação da empresa Infineon.

As simulações são realizadas utilizando a topologia de inversor trifásico de 2 níveis, conforme a imagem abaixo:

![](src/images/inverter.png)

## Tutorial

As instruções abaixo vão apresentar as informações necessárias para instalar e rodar o programa corretamente.

### Pré-requisitos

Para rodar esse programa é necessário ter o Mozilla Firefox versão 60 ou superior que pode ser baixado [neste link](https://www.mozilla.org/pt-BR/firefox/new/).

### Instalação

Baixe e instale o arquivo disponível [neste link](https://www.dropbox.com/sh/lt8700hnuhdy7km/AAAf3Y26jIrxC3CnyxlRQFg2a).

### Utilizando o programa

1. Abra o programa a partir do atalho gerado na área de trabalho.

2. Utilizando o botão **"Select input file"**, selecione o arquivo com a tabela contendo as informações das simulações que deseja rodar. Um arquivo de exemplo é disponibilizado na pasta **"examples"** no local onde o programa foi instalado. É importante que os nomes das colunas pré-existentes no arquivo de simulação <ins>não sejam alterados</ins>. 

3. Utilize o botão **"Select output folder"** para definir em qual pasta será salvo o arquivo com os resultados de simulação.

4. Insira seus dados de login do site do Iposim nos campos **"Iposim e-mail"** e **"Iposim password"**. Caso não tenha uma conta, é possível criar uma nova [neste link](https://www.infineon.com/cms/en/#register).

5. Após entrar com os dados, utilize o botão **"Simulate"** e aguarde a finalização da simulação observando as informações na tela. Ao final, o arquivo de resultados estará disponibilizado na pasta escolhida.

![](src/images/example.png)

## Autores

* **Alex Costa Machado**
