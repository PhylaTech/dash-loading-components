import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import '../../premium-styles';
import { OrbitRings as Upstream } from 'premium-react-loaders';

/**
 * PremiumOrbitRings — Dash wrapper for upstream OrbitRings.
 * Requires premium-react-loaders CSS (see ./styles).
 */
const PremiumOrbitRings = (props) => {
    const {id, className, style, size, color, speed, reverse, secondary_color, visible, thickness, ring_count, ring_gap, alternate, playing} = props;
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
                ringCount={ring_count}
                ringGap={ring_gap}
                alternate={alternate}
                className={wrapperClass(className, playing)} {...contract('premium', 'OrbitRings', props)} />
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
    secondary_color: PropTypes.string,
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
    ring_count: PropTypes.number,
    /**
     * Gap between rings in px.
     */
    ring_gap: PropTypes.number,
    /**
     * Alternate ring rotation directions.
     */
    alternate: PropTypes.bool,
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

export default PremiumOrbitRings;
