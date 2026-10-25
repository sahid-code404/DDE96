# Glasswave Design System

## 1. Design Philosophy
The Glasswave Design System translates the tactile clarity, refined materials, smooth physics, and disciplined typography of modern macOS into a cohesive, native Linux desktop experience.
It emphasizes:
- **Translucent Materials:** Multi-layered frosted glass surfaces with high-clarity backdrop blur and crisp border separation.
- **Traffic Light Controls:** Clean window management controls on the top-left (Close `#FF5F56`, Minimize `#FFBD2E`, Maximize `#27C93F`).
- **Harmonious Squircles:** Application icons and containers formatted with continuous curvature squircles.
- **Vibrant Accent Colors:** High-contrast semantic accents that adapt seamlessly between Light and Dark appearances.

## 2. Color Palette & Semantic Roles

| Token | Light Value | Dark Value | Semantic Purpose |
|:---|:---|:---|:---|
| `accent-primary` | `#007AFF` | `#0A84FF` | Primary interactive elements, selections, active toggles |
| `accent-purple` | `#5856D6` | `#5E5CE6` | Secondary accent, creative utilities |
| `accent-green` | `#34C759` | `#30D158` | Success state, window maximize button |
| `accent-orange` | `#FF9500` | `#FF9F0A` | Warning state, calculator operators, window minimize |
| `accent-red` | `#FF3B30` | `#FF453A` | Destructive action, window close button |
| `surface-panel` | `rgba(255,255,255,0.75)` | `rgba(28,28,30,0.78)` | Dock, top menu bar, headerbars |
| `surface-popover` | `rgba(255,255,255,0.85)` | `rgba(44,44,46,0.85)` | Quick settings, context menus, search popovers |
| `surface-modal` | `rgba(255,255,255,0.92)` | `rgba(30,30,32,0.92)` | Dialogs, preferences panes |
| `surface-opaque-fallback` | `#FFFFFF` | `#1C1C1E` | High-contrast or blur-disabled surfaces |
| `border-glass` | `rgba(255,255,255,0.40)` | `rgba(255,255,255,0.12)` | Subtle glass edge highlights |

## 3. Typography Hierarchy
Primary font family: `Inter`, `SF Pro Display`, `Cantarell`, `sans-serif`.
Monospace font family: `SF Mono`, `JetBrains Mono`, `Hack`, `monospace`.

- **Display Large:** 24px / 1.2 line-height, bold.
- **Title 1:** 18px / 1.25 line-height, semi-bold.
- **Title 2:** 15px / 1.3 line-height, medium.
- **Body Regular:** 13px / 1.4 line-height, normal.
- **Caption / Subhead:** 11px / 1.35 line-height, regular.

## 4. Corner Radii & Elevation Shadows
- **Radius S (6px):** Badges, small pills, menu items.
- **Radius M (10px):** Buttons, text inputs, list rows.
- **Radius L (16px):** Cards, popovers, alert dialogs.
- **Radius Dock (24px):** Floating bottom dock pill container.
- **Radius Squircle (22.5%):** Application icon silhouettes.

- **Elevation 1 (Subtle):** `0 2px 8px rgba(0,0,0,0.12)` - Floating buttons, cards.
- **Elevation 2 (Floating Bar):** `0 4px 16px rgba(0,0,0,0.18)` - Top bar, floating dock.
- **Elevation 3 (Popovers):** `0 12px 32px rgba(0,0,0,0.28)` - Quick settings, context menus.
- **Elevation 4 (Modal):** `0 24px 64px rgba(0,0,0,0.40)` - Application windows, alert dialogs.
