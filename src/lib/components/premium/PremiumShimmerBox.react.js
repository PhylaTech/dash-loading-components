import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import '../../premium-styles';
import { ShimmerBox as Upstream } from 'premium-react-loaders';

/**
 * PremiumShimmerBox — Dash wrapper for upstream spinner.
 *
 * Upstream ShimmerBox takes width/height (defaults 200x100) and baseColor.
 * `size` and `color` map onto those so the box behaves like every other
 * dlc component.
 */
const PremiumShimmerBox = (props) => {
    const {id, className, style, size, color, speed, secondary_color, visible, width, height, playing} = props;

    // size -> width/height at upstream's own 2:1, unless given outright.
    const upstreamProps = {speed, visible, className: wrapperClass(className, playing)};
    if (width !== undefined) {
        upstreamProps.width = width;
    } else if (size !== undefined) {
        upstreamProps.width = Math.round(Number(size) * 2);
    }
    if (height !== undefined) {
        upstreamProps.height = height;
    } else if (size !== undefined) {
        upstreamProps.height = Number(size);
    }
    if (color) {
        upstreamProps.baseColor = color;
    }
    if (secondary_color) {
        upstreamProps.highlightColor = secondary_color;
    }

    return (
        <div id={id} style={style}>
            <Upstream {...upstreamProps} {...contract('premium', 'ShimmerBox', props)} />
        </div>
    );
};

PremiumShimmerBox.defaultProps = {};

PremiumShimmerBox.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,
    /**
     * CSS class applied to the outer wrapper.
     */
    className: PropTypes.string,
    /**
     * Inline styles applied to the outer wrapper.
     */
    style: PropTypes.object,
    /**
     * Common API size. Mapped to width≈2×size and height≈size when
     * width/height are not set (upstream defaults are 200×100).
     */
    size: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    /**
     * Explicit box width (px or CSS length). Overrides size-derived width.
     */
    width: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    /**
     * Explicit box height (px or CSS length). Overrides size-derived height.
     */
    height: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    /**
     * Mapped to upstream baseColor (fill behind the shimmer).
     */
    color: PropTypes.string,
    /**
     * Speed (slow/normal/fast or duration token).
     */
    speed: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    /**
     * Mapped to upstream highlightColor (shimmer highlight).
     */
    secondary_color: PropTypes.string,
    /**
     * Whether the loader is visible.
     */
    visible: PropTypes.bool,
    /**
     * Relative tempo: 1.0 is this spinner's own tempo, 2.0 twice as fast,
     * 0.5 half. Leave unset to keep the upstream tempo.
     */
    rate: PropTypes.number,
    /**
     * Set to False to pause the animation.
     */
    playing: PropTypes.bool,
};

export default PremiumShimmerBox;
