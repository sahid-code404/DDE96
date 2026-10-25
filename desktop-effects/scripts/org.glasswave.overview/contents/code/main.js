// Glasswave KWin Overview Script
// Binds Meta+W / Meta+Tab to toggle KWin's Overview effect smoothly

registerShortcut("Glasswave Overview", "Toggle Mission Control Style Overview", "Meta+W", function () {
    workspace.slotToggleOverview();
});
