import React from 'react';
import PropTypes from 'prop-types';
import '../../premium-styles';
import { SpinnerCircle as Upstream } from 'premium-react-loaders';

/**
 * PremiumSpinnerCircle — Dash wrapper for upstream spinner.
 */
const PremiumSpinnerCircle = (props) => {
    const {id, className, style, setProps, size, color, speed, reverse, secondaryColor, visible, thickness} = props;
    return (
        <div id={id} style={style}>
            <Upstream size={size} color={color} speed={speed} reverse={reverse} secondaryColor={secondaryColor} visible={visible} thickness={thickness} className={className} />
        </div>
    );
};

PremiumSpinnerCircle.defaultProps = {};

PremiumSpinnerCircle.propTypes = {
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
    secondaryColor: PropTypes.string,
    /**
     * Whether the loader is visible.
     */
    visible: PropTypes.bool,
    /**
     * Stroke thickness.
     */
    thickness: PropTypes.number,
};

export default PremiumSpinnerCircle;
