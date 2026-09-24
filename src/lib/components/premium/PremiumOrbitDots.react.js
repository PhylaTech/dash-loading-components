import React from 'react';
import PropTypes from 'prop-types';
import '../../premium-styles';
import { OrbitDots as Upstream } from 'premium-react-loaders';

/**
 * PremiumOrbitDots — Dash wrapper for upstream OrbitDots.
 * Requires premium-react-loaders CSS (see ./styles).
 */
const PremiumOrbitDots = (props) => {
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
        dotCount,
        dotSize,
        orbitRadius,
        stagger,
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
                dotCount={dotCount}
                dotSize={dotSize}
                orbitRadius={orbitRadius}
                stagger={stagger}
                className={className}
            />
        </div>
    );
};

PremiumOrbitDots.defaultProps = {};

PremiumOrbitDots.propTypes = {
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
     * Secondary color for alternating dots.
     */
    secondaryColor: PropTypes.string,
    /**
     * Whether the loader is visible.
     */
    visible: PropTypes.bool,
    /**
     * Thickness of orbit path / elements.
     */
    thickness: PropTypes.number,
    /**
     * Number of orbiting dots.
     */
    dotCount: PropTypes.number,
    /**
     * Size of each dot.
     */
    dotSize: PropTypes.number,
    /**
     * Orbit radius relative to size.
     */
    orbitRadius: PropTypes.number,
    /**
     * Stagger animation between dots.
     */
    stagger: PropTypes.bool,
};

export default PremiumOrbitDots;
