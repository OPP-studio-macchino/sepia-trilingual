# Sepia Trilingual

[English](README.md) | [日本語](README.ja.md) | **Español**

Sepia Trilingual amplía Sepia con capas editoriales específicas para japonés, inglés y español.

Es un proyecto derivado e independiente de [Sepia de Nanako Tsai](https://github.com/Nanako0129/sepia), no una versión oficial. No implica respaldo, mantenimiento ni aprobación por parte de la autora original.

No pretende disfrazar un texto ni garantizar que supere detectores. Su objetivo es conservar hechos, intención, voz, registro, tratamiento y variedad regional mientras reduce explicaciones innecesarias y estructuras demasiado uniformes.

> No conviertas al autor en una versión supuestamente mejor. Haz que se entienda mejor sin hacerlo sonar como otra persona.

## Idiomas

- Japonés: `ja-JP`
- Inglés: conserva la variedad observada, como `en-US` o `en-GB`
- Español: conserva `tú / usted / vos`, `vosotros / ustedes` y el léxico regional

No traduce ni neutraliza la variedad regional sin una instrucción expresa.

## Cuatro operaciones

| Operación | Contrato |
|---|---|
| `write` | Crear un texto nuevo |
| `review` | Diagnosticar sin editar |
| `refactor` | Corregir lo mínimo y conservar estructura y voz |
| `recreate` | Reescribir desde los hechos, la intención y los rasgos de voz |

En Codex se usan `$sepia-write`, `$sepia-review`, `$sepia-refactor` y `$sepia-recreate`.

## Cómo se evalúa la voz

No se inventa una puntuación de “humanidad”. Se informa si se conservaron:

- el significado y los hechos;
- la voz del autor;
- el registro y la relación social;
- la variedad regional;
- el grado de certeza y la temperatura emocional.

Está prohibido añadir erratas, experiencias falsas, emociones inventadas, muletillas o jerga para simular humanidad.

## Configurar la voz sin delegarla por completo a la IA

Puedes entregar un perfil explícito basado en `examples/voice-profile.example.yaml`. Completa solo los campos que conozcas: tratamiento, formalidad, ritmo, expresiones que deben conservarse y cambios prohibidos.

Sepia no busca ni carga perfiles automáticamente. El perfil solo se usa cuando el usuario lo proporciona o autoriza un archivo concreto, y nunca puede sustituir los hechos, las citas, el código, la seguridad ni la instrucción actual. La especificación está en `skills/sepia/references/voice-profile-config.md`.

## Integración MCP opcional

El [servidor MCP de solo lectura](sepia_mcp/README.md) ofrece las reglas existentes de Sepia. No recibe borradores ni modifica textos.

El paquete para ChatGPT Web contiene solo skills, sin MCP. Consulta la [guía de instalación y requisitos de acceso (en inglés)](CHATGPT.md). La instalación y ejecución en la web todavía no se han probado.

## Instalación

Para Codex, después de publicar el repositorio:

```bash
codex plugin marketplace add OPP-studio-macchino/sepia-trilingual
codex plugin add sepia@sepia
```

Con Skills CLI:

```bash
npx skills add OPP-studio-macchino/sepia-trilingual -g
```

## Validación

```bash
python3 scripts/check_versions.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Autoría original y licencia

Este proyecto deriva de Sepia, creado por Nanako Tsai y publicado bajo la licencia MIT. Consulta [ATTRIBUTION.md](ATTRIBUTION.md) y `LICENSE`.
