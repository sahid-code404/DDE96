# Glasswave Interaction & Motion Guidelines

## 1. Motion Principles
Glasswave motion is purposeful, responsive, and physically grounded. Animations provide direct spatial context and confirmation rather than decorative delays.

## 2. Animation Curves & Durations
- **Standard Easing:** `cubic-bezier(0.25, 0.1, 0.25, 1.0)` (Smooth deceleration).
- **Spring / Bounce Easing:** `cubic-bezier(0.34, 1.56, 0.64, 1.0)` (App launch bounce, modal pop).
- **Fast Feedback (Buttons, Toggles):** 120ms.
- **Normal Transitions (Popovers, Navigation):** 200ms.
- **Window Transitions (Overview, Minimize):** 280ms.
- **Reduced Motion Override:** When `reduced_motion` is enabled in Glasswave Settings, all transitions drop to 0ms or a subtle instant crossfade (40ms), completely disabling scales, bounces, and translations.

## 3. Dock Physics
- **Pointer Magnification:**
  - Active when cursor enters dock threshold (within 24px of dock boundary).
  - Uses cosine bell-curve magnification factor:
    $$f(d) = 1.0 + M \cdot \cos^2\left(\frac{\pi d}{2 W}\right)$$
    where $d$ is distance in pixels from cursor, $W$ is effect width (72px), and $M$ is configured zoom factor (default 0.4, yielding max 1.4x scale).
- **App Launch Feedback:** Clicking a dock icon triggers an immediate bounce animation (3 gentle oscillations over 600ms) until the window surface is mapped.
- **Running Indicator:** A crisp 4px glowing dot rests below running application icons. Active focused application displays a brighter, slightly elongated indicator pill.

## 4. Window Decoration Interactions
- **Traffic Light Controls:**
  - Rest at top-left of the window titlebar.
  - Neutral state displays flat pastel colors (Red, Amber, Green).
  - Hovering anywhere within the 3-button cluster reveals subtle glyph icons inside all three buttons simultaneously (x for close, - for minimize, + for maximize).
  - Clicking triggers immediate window action with zero lag.
