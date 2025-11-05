IT_SETUP_GUIDE.md</path>
<content"># 🔧 Configuração Git para Evitar Warnings LF/CRLF

## 🚨 Problema Identificado

Warnings constantes ao fazer commits:
```
warning: in the working copy of 'arquivo.md', LF will be replaced by CRLF the next time Git touches it
```

## ✅ Solução Definitiva

### 1. Configuração Git Global

Execute estes comandos no terminal (uma vez):

```bash
# Configuração global para Windows
git config --global core.autocrlf input
git config --global core.safecrlf true
git config --global core.eol lf

# Configuração local para o repositório atual
git config --local core.autocrlf input
git config --local core.safecrlf true
```

### 2. Ficheiro .gitattributes

O ficheiro `.gitattributes` já foi criado com configurações específicas:

```gitattributes
# Normalização universal
* text=auto

# Ficheiros específicos
*.txt text eol=lf
*.md text eol=lf
*.py text eol=lf
*.js text eol=lf
*.html text eol=lf
*.css text eol=lf
*.json text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
*.sh text eol=lf
*.bat text eol=crlf
*.ps1 text eol=crlf
```

### 3. Aplicar Configurações

Para aplicar as configurações a todos os ficheiros existentes:

```bash
# Remover todos os ficheiros do índice (não delete ficheiros)
git rm --cached -r .

# Adicionar novamente com as novas configurações
git add .

# Fazer commit com as correções
git commit -m "fix: normalização de quebras de linha LF/CRLF

- Configurações Git aplicadas: autocrlf=input, safecrlf=true
- .gitattributes criado para normalização consistente
- Todos os ficheiros com quebras de linha LF
- Ficheiros .bat e .ps1 mantêm CRLF (Windows)"
```

## 🎯 Resultado Esperado

✅ **Sem mais warnings de quebras de linha**
✅ **Quebras de linha consistentes (LF)**
✅ **Compatibilidade cross-platform**
✅ **Configuração permanente para todos os projetos**

## 🔄 Para Novos Projetos

Sempre que criar um novo projeto:

1. **Configurar Git corretamente desde o início:**
   ```bash
   git config --local core.autocrlf input
   git config --local core.safecrlf true
   ```

2. **Criar .gitattributes imediatamente:**
   ```bash
   echo "* text=auto" > .gitattributes
   echo "*.md text eol=lf" >> .gitattributes
   echo "*.py text eol=lf" >> .gitattributes
   echo "*.js text eol=lf" >> .gitattributes
   echo "*.html text eol=lf" >> .gitattributes
   ```

3. **Commit inicial com .gitattributes:**
   ```bash
   git add .gitattributes
   git commit -m "feat: configuração inicial com .gitattributes"
   ```

## 📋 Checklist Final

- [x] Configuração Git global aplicada
- [x] .gitattributes criado e configurado
- [x] Ficheiros normalizados
- [x] Repositório enviado para GitHub
- [x] Sem warnings de quebras de linha

---

**Status**: ✅ Resolvido permanentemente
**Data**: 2025-11-05
**Projeto**: freqtrade2 (https://github.com/smpsandro1239/freqtrade2)
