import React, {useEffect, useState} from 'react';
import PropTypes from 'prop-types';
import {ThinkingOrb} from 'thinking-orbs';
import {wrapperClass} from '../../contract';

/**
 * ThinkingOrbsOrb -- Dash wrapper for thinking-orbs' dotted canvas orbs.
 *
 * `rate` maps to upstream `speed` as: speed = rate (both multiply the state's
 * baked tempo). `playing` maps to `paused = !playing`.
 *
 * Upstream draws each state from three hand-tuned designs, at 64, 32 and 20
 * px, and throws on any other size. `size` is therefore any pixel size: the
 * nearest design (in log space, since they differ by ratios) is drawn and the
 * canvas is scaled to `size` by CSS. 32 is interpolated by upstream from the
 * other two and has not had a tuning pass of its own.
 *
 * `theme="auto"` is upstream's: an ancestor `data-theme` attribute or `dark` /
 * `light` class, else the operating system. Mantine writes neither, so while
 * the page carries `data-mantine-color-scheme` on <html> this wrapper mirrors
 * it onto its own `data-theme` for upstream to read.
 */
const LARGE = 64;
const MEDIUM = 32;
const SMALL = 20;
const DESIGNS = [LARGE, MEDIUM, SMALL];
const DEFAULT_SIZE = LARGE;

const nearestDesign = (px) => DESIGNS.reduce(
    (best, d) => (Math.abs(Math.log(px / d)) < Math.abs(Math.log(px / best)) ? d : best)
);

const readMantineScheme = () => {
    if (typeof document === 'undefined') {
        return undefined;
    }
    const scheme = document.documentElement.getAttribute('data-mantine-color-scheme');
    return scheme === 'dark' || scheme === 'light' ? scheme : undefined;
};

const useMantineScheme = () => {
    const [scheme, setScheme] = useState(readMantineScheme);
    useEffect(() => {
        const observer = new MutationObserver(() => setScheme(readMantineScheme()));
        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['data-mantine-color-scheme'],
        });
        return () => observer.disconnect();
    }, []);
    return scheme;
};

const ThinkingOrbsOrb = (props) => {
    const {
        id, className, style,
        state, size, theme, speed, paused, color, dots, dot_size, aria_label,
        rate, playing,
    } = props;

    const mantineScheme = useMantineScheme();

    const px = size > 0 ? size : DEFAULT_SIZE;
    const resolvedSpeed = speed !== undefined && speed !== null ? speed
        : (rate !== undefined && rate !== null ? rate : undefined);
    const resolvedPaused = paused !== undefined && paused !== null ? paused
        : (playing !== undefined && playing !== null ? !playing : undefined);

    const orb = {
        state,
        size: nearestDesign(px),
        theme,
        speed: resolvedSpeed,
        paused: resolvedPaused,
        color: color || undefined,
        dots,
        dotSize: dot_size,
        'aria-label': aria_label,
        style: {width: px, height: px},
    };
    Object.keys(orb).forEach((key) => orb[key] === undefined && delete orb[key]);

    return (
        <div
            id={id}
            className={wrapperClass(className, playing)}
            style={{width: 'fit-content', ...style}}
            data-theme={!theme || theme === 'auto' ? mantineScheme : undefined}
        >
            <ThinkingOrb {...orb} />
        </div>
    );
};

ThinkingOrbsOrb.defaultProps = {};

ThinkingOrbsOrb.propTypes = {
    /** The ID used to identify this component in Dash callbacks. */
    id: PropTypes.string,
    /** CSS class applied to the outer wrapper. */
    className: PropTypes.string,
    /** Inline styles applied to the outer wrapper. */
    style: PropTypes.object,

    /**
     * Which orb animation to show: "working", "searching", "solving",
     * "listening", "connecting", "weaving", "composing", "breathing" or
     * "shaping". Defaults to "working".
     */
    state: PropTypes.oneOf([
        'working', 'searching', 'solving', 'listening', 'connecting',
        'weaving', 'composing', 'breathing', 'shaping',
    ]),
    /**
     * Square canvas side in CSS pixels. Upstream has three designs, at 64
     * (chat avatar), 32 and 20 (inline text); the nearest one is drawn and
     * scaled to this size. Sizes above 64 upscale the 64 design, so they
     * soften. Default 64.
     */
    size: PropTypes.number,
    /**
     * Ink for the dots: "auto", "dark" or "light". Dark is light ink for dark
     * backgrounds; light is dark ink for light ones. "auto" follows an
     * ancestor data-theme attribute or dark/light class, the Mantine colour
     * scheme, or else the operating system. Default "auto".
     */
    theme: PropTypes.oneOf(['auto', 'dark', 'light']),
    /**
     * Upstream tempo multiplier on the state's own speed. 1 = normal. Prefer
     * `rate` for the common contract; an explicit `speed` wins over `rate`.
     */
    speed: PropTypes.number,
    /**
     * Upstream pause flag. When `playing` is set and `paused` is not,
     * paused = !playing. An explicit `paused` wins.
     */
    paused: PropTypes.bool,
    /**
     * Optional ink tint as "#rgb", "#rrggbb" or "rgb(r, g, b)"; any other
     * CSS colour syntax is ignored by upstream. The orb's depth shading is
     * kept on the tint. Leave unset for the stock monochrome ink.
     */
    color: PropTypes.string,
    /**
     * Dot-count multiplier, applied while keeping the state's balance.
     * 1 (default) is the tuned look; upstream floors it at 0.1.
     */
    dots: PropTypes.number,
    /**
     * Dot-radius multiplier. 1 (default) is the tuned look; 0.7 reads finer,
     * 1.5 bolder. Upstream floors it at 0.1.
     */
    dot_size: PropTypes.number,
    /**
     * Accessible label on the canvas. Defaults to a per-state label such as
     * "Searching...".
     */
    aria_label: PropTypes.string,

    /**
     * Relative tempo: 1.0 is the state's own tempo, 2.0 twice as fast.
     * Mapped to upstream speed = rate. Leave unset to keep the default.
     */
    rate: PropTypes.number,
    /** Set to False to freeze the animation on its current frame. */
    playing: PropTypes.bool,
};

export default ThinkingOrbsOrb;
