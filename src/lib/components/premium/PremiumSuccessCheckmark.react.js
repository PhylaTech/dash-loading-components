import React from 'react';
import PropTypes from 'prop-types';
import { SuccessCheckmark as Upstream } from 'premium-react-loaders';

/**
 * PremiumSuccessCheckmark — Dash wrapper for upstream spinner.
 */
const PremiumSuccessCheckmark = (props) => {
    const {id, className, style, setProps, size, color, speed, secondaryColor, visible} = props;
    return (
        <div id={id} style={style}>
            <Upstream size={size} color={color} speed={speed}  secondaryColor={secondaryColor} visible={visible} className={className} />
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
     * Secondary color for multi-color loaders.
     */
    secondaryColor: PropTypes.string,
    /**
     * Whether the loader is visible.
     */
    visible: PropTypes.bool,
};

export default PremiumSuccessCheckmark;
