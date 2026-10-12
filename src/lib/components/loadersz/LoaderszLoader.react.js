import React from 'react';
import PropTypes from 'prop-types';
import {wrapperClass} from '../../contract';
import {registerLoadersz} from 'loadersz';

registerLoadersz();

/**
 * LoaderszLoader -- Dash wrapper for loadersz's canvas-based loading indicators.
 *
 * loadersz ships as a native Web Component (`<loadersz-loader>`). This wrapper
 * renders the custom element, forwarding Dash-friendly snake_case props to its
 * kebab-case attributes and managing the common dlc contract (rate, playing).
 *
 * `rate` maps to upstream `speed` as: speed = rate (both are multipliers).
 * `size` maps directly (upstream also calls it `size`, CSS px).
 * `color` maps directly (upstream also calls it `color`, CSS colour string).
 */
const LoaderszLoader = (props) => {
    const {
        id, className, style,
        state, size, speed, density, particle_radius,
        theme, hue, color, paused, force_motion, aria_label,
        rate, playing,
    } = props;

    const resolvedSpeed = speed !== undefined ? speed
        : (rate !== undefined && rate !== null ? rate : undefined);

    const resolvedPaused = paused !== undefined ? paused
        : (playing !== undefined && playing !== null ? !playing : undefined);

    const attrs = {};
    if (state !== undefined) {
        attrs.state = state;
    }
    if (size !== undefined) {
        attrs.size = String(size);
    }
    if (resolvedSpeed !== undefined) {
        attrs.speed = String(resolvedSpeed);
    }
    if (density !== undefined) {
        attrs.density = String(density);
    }
    if (particle_radius !== undefined) {
        attrs['particle-radius'] = String(particle_radius);
    }
    if (theme !== undefined) {
        attrs.theme = theme;
    }
    if (hue !== undefined) {
        attrs.hue = String(hue);
    }
    if (color !== undefined) {
        attrs.color = color;
    }
    if (resolvedPaused === true) {
        attrs.paused = '';
    }
    if (force_motion === true) {
        attrs['force-motion'] = '';
    }
    if (aria_label !== undefined) {
        attrs['aria-label'] = aria_label;
    }

    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            <loadersz-loader {...attrs} />
        </div>
    );
};

LoaderszLoader.defaultProps = {};

LoaderszLoader.propTypes = {
    /** The ID used to identify this component in Dash callbacks. */
    id: PropTypes.string,
    /** CSS class applied to the outer wrapper. */
    className: PropTypes.string,
    /** Inline styles applied to the outer wrapper. */
    style: PropTypes.object,

    /**
     * Which loader animation to show. One of the 160 semantic state names
     * (e.g. "working", "searching", "heatmapping"). Defaults to "working".
     */
    state: PropTypes.string,
    /**
     * Square canvas side in CSS pixels. Values below 16 are clamped by
     * upstream. Default 96.
     */
    size: PropTypes.number,
    /**
     * Upstream timeline multiplier. 1 = normal speed. Prefer `rate` for the
     * common contract; an explicit `speed` wins over `rate`.
     */
    speed: PropTypes.number,
    /** Geometry detail multiplier. Clamped to 0.35-2 by upstream. Default 1. */
    density: PropTypes.number,
    /** Particle thickness multiplier. Clamped to 0.5-2.5 by upstream. Default 1. */
    particle_radius: PropTypes.number,
    /** Canvas colour scheme: "auto", "dark", or "light". Default "auto". */
    theme: PropTypes.oneOf(['auto', 'dark', 'light']),
    /** Overrides native colour palette with a single hue (0-360). */
    hue: PropTypes.number,
    /** CSS colour string. Overrides hue when set. */
    color: PropTypes.string,
    /**
     * Upstream pause flag. When `playing` is set and `paused` is not,
     * paused = !playing. An explicit `paused` wins.
     */
    paused: PropTypes.bool,
    /** Override reduced-motion preference. */
    force_motion: PropTypes.bool,
    /** Accessible label on the canvas. Default "Loading". */
    aria_label: PropTypes.string,

    /**
     * Relative tempo: 1.0 is normal speed, 2.0 twice as fast.
     * Mapped to upstream speed = rate. Leave unset to keep the default.
     */
    rate: PropTypes.number,
    /** Set to False to pause the animation. */
    playing: PropTypes.bool,
};

export default LoaderszLoader;
