# Preparar o ambiente:

## Instalar nvm:
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

## Instala Node.js e npm:
```
nvm install --lts
```

## Instalar o Ionic CLI:
```
npm install -g @ionic/cli
```

### Verificar instalações:
```
node -v

npm -v

ionic -v
```

## Iniciar o ambiente Ionic:
```
ionic start outoftheloop blank --type=react --capacitor
```

## Abrir o terminal na raiz do projeto:
```
cd outoftheloop
```
 

### Rodar aplicação:

*Abra o terminal na pasta raiz do projeto (outoftheloop) e rode o seguinte comando*

```
ionic serve
```

## Build da aplicação:

*No diretório raiz*

```
ionic build
```

```
npx cap sync android
```

*Entrar no diretório android*
```
cd android
```

*Iniciar build*
```
./gradlew assembleDebug
```

