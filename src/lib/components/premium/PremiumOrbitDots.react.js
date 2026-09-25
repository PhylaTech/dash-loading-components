import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import '../../premium-styles';
import { OrbitDots as Upstream } from 'premium-react-loaders';

/**
 * PremiumOrbitDots — Dash wrapper for upstream OrbitDots.
 * Requires premium-react-loaders CSS (see ./styles).
 */
const PremiumOrbitDots = (props) => {
    const {id, className, style, size, color, speed, reverse, secondary_color, visible, thickness, dot_count, dot_size, orbit_radius, stagger, playing} = props;
    return (
        <div id={id} style={style}>
            <Upstream
                size={size}
                color={color}
                speed={speed}
                reverse={reverse}
                secondaryColor={secondary_color}
                visible={visible}
                thickness={thickness}
                dotCount={dot_count}
                dotSize={dot_size}
                orbitRadius={orbit_radius}
                stagger={stagger}
                className={wrapperClass(className, playing)} {...contract('premium', 'OrbitDots', props)} />
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
    secondary_color: PropTypes.string,
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
    dot_count: PropTypes.number,
    /**
     * Size of each dot.
     */
    dot_size: PropTypes.number,
    /**
     * Orbit radius relative to size.
     */
    orbit_radius: PropTypes.number,
    /**
     * Stagger animation between dots.
     */
    stagger: PropTypes.bool,
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

export default PremiumOrbitDots;
