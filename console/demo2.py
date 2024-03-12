#!/usr/bin/env python3

from rich.console import Console

console = Console(width=20)

style = 'italic bold white on blue'

console.print('Rich', style=style)
console.print('Rich', style=style, justify='left')
console.print('Rich', style=style, justify='center')
console.print('Rich', style=style, justify='right')
