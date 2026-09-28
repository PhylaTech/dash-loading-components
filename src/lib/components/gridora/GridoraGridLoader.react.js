import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import {GridLoader as Upstream, GRID_LOADER_DEFAULTS} from 'gridora';
import 'gridora/styles.css';

const DEFAULTS = GRID_LOADER_DEFAULTS;

/**
 * GridoraGridLoader — Dash wrapper for gridora's GridLoader.
 *
 * Common `size` is overall CSS px, NOT upstream `size`/`cellSize` (which is
 * cell px). When common `size` is set and `cell_size` is not, we derive
 * `cellSize = (size - (gridSize - 1) * gap) / gridSize`, clamped ≥ 1.
 */
const GridoraGridLoader = (props) => {
    const {
        id, className, style,
        variant, sequence, mask, grid_size, cell_size, dot_size, gap,
        speed, color, colors, color_mode, effect, shape, easing,
        inactive, inactive_opacity, inactive_color,
        min_opacity, max_opacity, min_scale, max_scale,
        glow, spread, offset, mask_motion, label,
        respect_reduced_motion, reverse, direction, paused, playing,
        size,
    } = props;

    const gridSize = grid_size ?? DEFAULTS.gridSize;
    const gapPx = gap ?? DEFAULTS.gap;

    let cellSize = cell_size;
    if (cellSize === undefined && size !== undefined) {
        cellSize = Math.max(1, (size - (gridSize - 1) * gapPx) / gridSize);
    }

    // Every upstream prop has a destructuring default, so an undefined prop
    // is the same as one left off: pass them all straight through.
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            <Upstream
                variant={variant}
                sequence={sequence}
                mask={mask}
                gridSize={gridSize}
                cellSize={cellSize}
                dotSize={dot_size}
                gap={gapPx}
                speed={speed}
                color={color}
                colors={colors}
                colorMode={color_mode}
                effect={effect}
                shape={shape}
                easing={easing}
                inactive={inactive}
                inactiveOpacity={inactive_opacity}
                inactiveColor={inactive_color}
                minOpacity={min_opacity}
                maxOpacity={max_opacity}
                minScale={min_scale}
                maxScale={max_scale}
                glow={glow}
                spread={spread}
                offset={offset}
                maskMotion={mask_motion}
                label={label}
                respectReducedMotion={respect_reduced_motion}
                reverse={reverse}
                direction={direction}
                paused={paused}
                {...contract('gridora', 'GridLoader', props)}
            />
        </div>
    );
};

GridoraGridLoader.defaultProps = {};

GridoraGridLoader.propTypes = {
    /** The ID used to identify this component in Dash callbacks. */
    id: PropTypes.string,
    /** CSS class applied to the outer wrapper. */
    className: PropTypes.string,
    /** Inline styles applied to the outer wrapper. */
    style: PropTypes.object,

    /**
     * Overall CSS pixel size (common contract). When set and `cell_size` is
     * unset, derives cellSize = (size - (gridSize-1)*gap) / gridSize. NOT
     * passed through as upstream `size`/`cellSize`.
     */
    size: PropTypes.number,
    /** Animation pattern (one of the 133 motion variants, or a glyph). */
    variant: PropTypes.string,
    /** Ordered cell indices for custom animation order. */
    sequence: PropTypes.arrayOf(PropTypes.number),
    /** Custom bitmap mask (array of arrays of 0/1, or a slash-delimited string). */
    mask: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.number)), PropTypes.string]),
    /** Number of rows and columns (2–12). Default 3. */
    grid_size: PropTypes.number,
    /** Size of each grid cell in pixels. Default 4. */
    cell_size: PropTypes.number,
    /** Size of the dot inside a cell in pixels. Default cellSize × 0.875. */
    dot_size: PropTypes.number,
    /** Space between cells in pixels. Default 2.5. */
    gap: PropTypes.number,
    /**
     * Upstream cycle duration in seconds. Higher = slower. Default 1.
     * When `rate` is set and `speed` is not, speed = 1/rate.
     */
    speed: PropTypes.number,
    /** Base color or first stop when colors is omitted. */
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
    /** Opacity at the resting point. Default 0.2. */
    min_opacity: PropTypes.number,
    /** Opacity at the peak. Default 1. */
    max_opacity: PropTypes.number,
    /** Scale at the resting point. Default 1. */
    min_scale: PropTypes.number,
    /** Scale at the peak. Default 1. */
    max_scale: PropTypes.number,
    /** Blur radius of the dot glow in pixels. Default 0. */
    glow: PropTypes.number,
    /** How much of the cycle the stagger spans (1 = full cycle). */
    spread: PropTypes.number,
    /** Extra phase offset in cycles. */
    offset: PropTypes.number,
    /** Drawing order for glyph and mask variants. */
    mask_motion: PropTypes.oneOf(['write', 'writeReverse', 'fade', 'sweepX', 'sweepY', 'diagonal', 'radial', 'random', 'wave', 'drop', 'typewriter']),
    /** Plays the stagger backwards. */
    reverse: PropTypes.bool,
    /** CSS animation direction. */
    direction: PropTypes.string,
    /** Accessible label. Default "Loading". */
    label: PropTypes.string,
    /** Disables animation when user prefers reduced motion. */
    respect_reduced_motion: PropTypes.bool,
    /**
     * Upstream `paused`. When `playing` is set and `paused` is not,
     * paused = !playing. An explicit `paused` wins.
     */
    paused: PropTypes.bool,
    /**
     * Relative tempo: 1.0 = 1 s/cycle, 2.0 = 0.5 s/cycle.
     * Mapped to upstream speed = 1/rate. Leave unset to keep the default.
     */
    rate: PropTypes.number,
    /** Set to False to pause the animation. */
    playing: PropTypes.bool,
};

export default GridoraGridLoader;
