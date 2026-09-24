import React from 'react';
import PropTypes from 'prop-types';
import '../../premium-styles';
import { ShimmerBox as Upstream } from 'premium-react-loaders';

/**
 * PremiumShimmerBox — Dash wrapper for upstream spinner.
 *
 * Upstream ShimmerBox uses width/height (defaults 200×100) and baseColor,
 * not the Common API `size`/`color`. Map those so gallery + dlc.Loading
 * size presets produce a box that fits preview frames.
 */
const PremiumShimmerBox = (props) => {
    const {
        id,
        className,
        style,
        setProps,
        size,
        color,
        speed,
        reverse,
        secondaryColor,
        visible,
        width,
        height,
    } = props;

    // Common API size → upstream width/height (2:1 aspect, matching upstream defaults).
    // Explicit width/height win when provided.
    let resolvedWidth = width;
    let resolvedHeight = height;
    if (size != null && size !== '') {
        const n = typeof size === 'number' ? size : Number(size);
        if (!Number.isNaN(n)) {
            if (resolvedWidth == null) {
                resolvedWidth = Math.round(n * 2);
            }
            if (resolvedHeight == null) {
                resolvedHeight = n;
            }
        }
    }

    const upstreamProps = {
        speed,
        visible,
        className,
    };
    if (resolvedWidth != null) {
        upstreamProps.width = resolvedWidth;
    }
    if (resolvedHeight != null) {
        upstreamProps.height = resolvedHeight;
    }
    if (color) {
        upstreamProps.baseColor = color;
    }
    if (secondaryColor) {
        upstreamProps.highlightColor = secondaryColor;
    }
    // reverse is not an upstream prop; direction could be flipped later if needed
    void reverse;
    void setProps;

    return (
        <div id={id} style={style}>
            <Upstream {...upstreamProps} />
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
     * Dash-assigned callback that should be called to report property changes.
     */
    setProps: PropTypes.func,
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
     * Reverse animation direction (reserved; upstream uses direction enum).
     */
    reverse: PropTypes.bool,
    /**
     * Mapped to upstream highlightColor (shimmer highlight).
     */
    secondaryColor: PropTypes.string,
    /**
     * Whether the loader is visible.
     */
    visible: PropTypes.bool,
};

export default PremiumShimmerBox;
