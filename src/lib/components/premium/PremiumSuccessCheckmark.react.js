import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import '../../premium-styles';
import { SuccessCheckmark as Upstream } from 'premium-react-loaders';

/**
 * PremiumSuccessCheckmark — Dash wrapper for upstream spinner.
 */
const PremiumSuccessCheckmark = (props) => {
    const {id, className, style, size, color, speed, secondary_color, visible, playing} = props;
    return (
        <div id={id} style={style}>
            <Upstream size={size} color={color} speed={speed}  secondaryColor={secondary_color} visible={visible} className={wrapperClass(className, playing)} {...contract('premium', 'SuccessCheckmark', props)} />
        </div>
    );
};

PremiumSuccessCheckmark.defaultProps = {};

PremiumSuccessCheckmark.propTypes = {
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

export default PremiumSuccessCheckmark;
