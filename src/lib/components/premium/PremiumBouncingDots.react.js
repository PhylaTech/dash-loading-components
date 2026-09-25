import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import '../../premium-styles';
import { BouncingDots as Upstream } from 'premium-react-loaders';

/**
 * PremiumBouncingDots — Dash wrapper for upstream spinner.
 */
const PremiumBouncingDots = (props) => {
    const {id, className, style, size, color, speed, reverse, secondary_color, visible, rate, playing} = props;
    return (
        <div id={id} style={style}>
            <Upstream size={size} color={color} speed={speed} reverse={reverse} secondaryColor={secondary_color} visible={visible} className={wrapperClass(className, playing)} {...contract('premium', 'BouncingDots', props)} />
        </div>
    );
};

PremiumBouncingDots.defaultProps = {};

PremiumBouncingDots.propTypes = {
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
     * Size (sm/md/lg or number).
     */
    size: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    /**
     * Color.
     */
    color: PropTypes.string,
    /**
     * Speed (slow/normal/fast).
     */
    speed: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    /**
     * Reverse animation direction.
     */
    reverse: PropTypes.bool,
    /**
     * Secondary color for multi-color loaders.
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

export default PremiumBouncingDots;
