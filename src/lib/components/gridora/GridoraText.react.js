import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import {GridLoaderText as Upstream, GRID_LOADER_DEFAULTS} from 'gridora';
import 'gridora/dist/styles.css';

const DEFAULTS = GRID_LOADER_DEFAULTS;

/**
 * GridoraText — Dash wrapper for gridora's GridLoaderText.
 *
 * Same tempo/color/effect surface as GridLoader, plus `text`, `letter_gap`,
 * `letter_span`, `simultaneous`. No `variant`/`mask`/`sequence`.
 */
const GridoraText = (props) => {
    const {
        id, className, style,
        text, letter_gap, letter_span, simultaneous,
        grid_size, cell_size, dot_size, gap,
        speed, color, colors, color_mode, effect, shape, easing,
        inactive, inactive_opacity, inactive_color,
        min_opacity, max_opacity, min_scale, max_scale,
        glow, mask_motion, label,
        respect_reduced_motion, reverse, direction, paused, playing,
        size,
    } = props;

    const gridSize = grid_size ?? DEFAULTS.gridSize;
    const gapPx = gap ?? DEFAULTS.gap;

    let cellSize = cell_size;
    if (cellSize === undefined && size !== undefined) {
        cellSize = Math.max(1, (size - (gridSize - 1) * gapPx) / gridSize);
    }

    const upstream = {text: text || ''};
    if (letter_gap !== undefined) upstream.letterGap = letter_gap;
    if (letter_span !== undefined) upstream.letterSpan = letter_span;
    if (simultaneous !== undefined) upstream.simultaneous = simultaneous;
    upstream.gridSize = gridSize;
    if (cellSize !== undefined) upstream.cellSize = cellSize;
    if (dot_size !== undefined) upstream.dotSize = dot_size;
    upstream.gap = gapPx;
    if (speed !== undefined) upstream.speed = speed;
    if (color !== undefined) upstream.color = color;
    if (colors !== undefined) upstream.colors = colors;
    if (color_mode !== undefined) upstream.colorMode = color_mode;
    if (effect !== undefined) upstream.effect = effect;
    if (shape !== undefined) upstream.shape = shape;
    if (easing !== undefined) upstream.easing = easing;
    if (inactive !== undefined) upstream.inactive = inactive;
    if (inactive_opacity !== undefined) upstream.inactiveOpacity = inactive_opacity;
    if (inactive_color !== undefined) upstream.inactiveColor = inactive_color;
    if (min_opacity !== undefined) upstream.minOpacity = min_opacity;
    if (max_opacity !== undefined) upstream.maxOpacity = max_opacity;
    if (min_scale !== undefined) upstream.minScale = min_scale;
    if (max_scale !== undefined) upstream.maxScale = max_scale;
    if (glow !== undefined) upstream.glow = glow;
    if (mask_motion !== undefined) upstream.maskMotion = mask_motion;
    if (label !== undefined) upstream.label = label;
    if (respect_reduced_motion !== undefined) upstream.respectReducedMotion = respect_reduced_motion;
    if (reverse !== undefined) upstream.reverse = reverse;
    if (direction !== undefined) upstream.direction = direction;
    if (paused !== undefined) upstream.paused = paused;

    const mapped = contract('gridora', 'Text', props);
    Object.assign(upstream, mapped);

    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            <Upstream {...upstream} />
        </div>
    );
};

GridoraText.defaultProps = {};

GridoraText.propTypes = {
    /** The ID used to identify this component in Dash callbacks. */
    id: PropTypes.string,
    /** CSS class applied to the outer wrapper. */
    className: PropTypes.string,
    /** Inline styles applied to the outer wrapper. */
    style: PropTypes.object,

    /** Text drawn with the bitmap font. Required. */
    text: PropTypes.string.isRequired,
    /** Space between glyphs in pixels. */
    letter_gap: PropTypes.number,
    /** Fraction of the cycle each glyph occupies. */
    letter_span: PropTypes.number,
    /** Draws every glyph at the same time instead of sequentially. */
    simultaneous: PropTypes.bool,

    /**
     * Overall CSS pixel size (common contract). When set and `cell_size` is
     * unset, derives cellSize from grid geometry. NOT passed as upstream
     * `size`/`cellSize`.
     */
    size: PropTypes.number,
    /** Number of rows and columns (2–12). Default 3. */
    grid_size: PropTypes.number,
    /** Size of each grid cell in pixels. Default 4. */
    cell_size: PropTypes.number,
    /** Size of the dot inside a cell in pixels. */
    dot_size: PropTypes.number,
    /** Space between cells in pixels. Default 2.5. */
    gap: PropTypes.number,
    /** Upstream cycle duration in seconds. Higher = slower. Default 1. */
    speed: PropTypes.number,
    /** Base color. */
    color: PropTypes.string,
    /** Color ramp sampled according to color_mode. */
    colors: PropTypes.arrayOf(PropTypes.string),
    /** How colors map onto the grid. */
    color_mode: PropTypes.oneOf(['solid', 'horizontal', 'vertical', 'diagonal', 'radial', 'angular', 'random', 'cycle']),
    /** Keyframes applied to every dot. */
    effect: PropTypes.oneOf(['pulse', 'fade', 'scale', 'blink', 'bounce', 'swing', 'flip', 'jelly', 'glow', 'spin', 'wobble', 'swell', 'drop', 'rise', 'zoom', 'pop', 'flicker', 'ping', 'twist', 'morph']),
    /** Dot silhouette. */
    shape: PropTypes.oneOf(['circle', 'square', 'rounded', 'squircle', 'diamond', 'triangle', 'hexagon', 'star', 'plus', 'ring', 'blob', 'bar']),
    /** CSS timing function. */
    easing: PropTypes.string,
    /** Rendering of cells not part of the shape. */
    inactive: PropTypes.oneOf(['dim', 'hidden', 'solid']),
    /** Opacity used when inactive is "dim". */
    inactive_opacity: PropTypes.number,
    /** Color used for inactive cells. */
    inactive_color: PropTypes.string,
    /** Opacity at the resting point. */
    min_opacity: PropTypes.number,
    /** Opacity at the peak. */
    max_opacity: PropTypes.number,
    /** Scale at the resting point. */
    min_scale: PropTypes.number,
    /** Scale at the peak. */
    max_scale: PropTypes.number,
    /** Blur radius of the dot glow in pixels. */
    glow: PropTypes.number,
    /** Drawing order for mask variants. */
    mask_motion: PropTypes.oneOf(['write', 'writeReverse', 'fade', 'sweepX', 'sweepY', 'diagonal', 'radial', 'random', 'wave', 'drop', 'typewriter']),
    /** Plays the stagger backwards. */
    reverse: PropTypes.bool,
    /** CSS animation direction. */
    direction: PropTypes.string,
    /** Accessible label. */
    label: PropTypes.string,
    /** Disables animation when user prefers reduced motion. */
    respect_reduced_motion: PropTypes.bool,
    /** Upstream `paused`. Explicit paused wins over playing. */
    paused: PropTypes.bool,
    /** Relative tempo: rate=1 → 1s/cycle, rate=2 → 0.5s/cycle. */
    rate: PropTypes.number,
    /** Set to False to pause the animation. */
    playing: PropTypes.bool,
};

export default GridoraText;
