import React from 'react';
import PropTypes from 'prop-types';
import '../../premium-styles';
import { OrbitRings as Upstream } from 'premium-react-loaders';

/**
 * PremiumOrbitRings — Dash wrapper for upstream OrbitRings.
 * Requires premium-react-loaders CSS (see ./styles).
 */
const PremiumOrbitRings = (props) => {
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
        thickness,
        ringCount,
        ringGap,
        alternate,
    } = props;
    return (
        <div id={id} style={style}>
            <Upstream
                size={size}
                color={color}
                speed={speed}
                reverse={reverse}
                secondaryColor={secondaryColor}
                visible={visible}
                thickness={thickness}
                ringCount={ringCount}
                ringGap={ringGap}
                alternate={alternate}
                className={className}
            />
        </div>
    );
};

PremiumOrbitRings.defaultProps = {};

PremiumOrbitRings.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,
    /**
     * CSS class applied to the upstream spinner root.
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
     * Size (xs/sm/md/lg/xl or number px).
     */
    size: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    /**
     * Primary color.
     */
    color: PropTypes.string,
    /**
     * Speed: 'slow' | 'normal' | 'fast' or duration in milliseconds.
     * Common API relative speed is translated to ms before reaching this prop.
     */
    speed: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    /**
     * Reverse animation direction.
     */
    reverse: PropTypes.bool,
    /**
     * Secondary color for alternating rings.
     */
    secondaryColor: PropTypes.string,
    /**
     * Whether the loader is visible.
     */
    visible: PropTypes.bool,
    /**
     * Ring border thickness in px.
     */
    thickness: PropTypes.number,
    /**
     * Number of concentric rings.
     */
    ringCount: PropTypes.number,
    /**
     * Gap between rings in px.
     */
    ringGap: PropTypes.number,
    /**
     * Alternate ring rotation directions.
     */
    alternate: PropTypes.bool,
};

export default PremiumOrbitRings;
