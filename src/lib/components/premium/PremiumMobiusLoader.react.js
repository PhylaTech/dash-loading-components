import React from 'react';
import PropTypes from 'prop-types';
import { MobiusLoader as Upstream } from 'premium-react-loaders';

/**
 * PremiumMobiusLoader — Dash wrapper for upstream spinner.
 */
const PremiumMobiusLoader = (props) => {
    const {id, className, style, setProps, size, color, speed} = props;
    return (
        <div id={id} className={className} style={style}>
            <Upstream size={size} color={color} speed={speed} />
        </div>
    );
};

PremiumMobiusLoader.defaultProps = {};

PremiumMobiusLoader.propTypes = {
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
    speed: PropTypes.string,
};

export default PremiumMobiusLoader;
