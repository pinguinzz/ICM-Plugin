# Component Registry

> **EXAMPLE.** Replace with your real component library.

Reusable Remotion components available to the production stage. Each entry: name, what it does, expected props.

## TitleCard
Full-screen text title with brand colors.
Props: `{ text: string, subtitle?: string, theme?: 'dark' | 'light' }`

## TalkingHead
Video of the host (PNG or video asset) with synced audio.
Props: `{ asset: string, audio: string, captions?: string[] }`

## CodeBlock
Syntax-highlighted code with line-by-line reveal.
Props: `{ language: string, code: string, highlight?: number[] }`

## DiagramFlow
Animated boxes-and-arrows diagram.
Props: `{ nodes: Node[], edges: Edge[], step?: number }`

## ListReveal
Bulleted list, items appear one by one.
Props: `{ items: string[], interval?: number }`

## QuoteBlock
Pull-quote in large type with attribution.
Props: `{ quote: string, attribution: string }`

## If you need a new component

Add a row above and a stub Remotion component to the project. Update this file. Run `/ICM-remap`.
