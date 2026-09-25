/**
 * Shared side-effect import for premium-react-loaders CSS.
 * Every premium Dash wrapper imports this file once so webpack/style-loader
 * injects the stylesheet whenever a premium chunk loads (dynamic import).
 * Identical module identity → CSS is not duplicated N times in the runtime.
 *
 * premium-fixes.css must come second: it overrides upstream keyframes by name.
 */
import 'premium-react-loaders/styles';
import './premium-fixes.css';
