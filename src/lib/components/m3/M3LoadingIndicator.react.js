import React from 'react';
import PropTypes from 'prop-types';
import { M3LoadingIndicator as Upstream } from '@alerix/m3-loading-indicator/react';

/**
 * M3LoadingIndicator — Dash wrapper for upstream spinner.
 */
const M3LoadingIndicator = (props) => {
    const {id, className, style, setProps, size, color, sizeRatio, speed, paused, contained, containerColor} = props;
    return (
        <div id={id} className={className} style={style}>
            <Upstream size={size} color={color} sizeRatio={sizeRatio} speed={speed} paused={paused} contained={contained} containerColor={containerColor} />
        </div>
    );
};

M3LoadingIndicator.defaultProps = {};

M3LoadingIndicator.propTypes = {
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
     * CSS pixel size (default 48).
     */
    size: PropTypes.number,
    /**
     * Fill color.
     */
    color: PropTypes.string,
    /**
     * Ratio of indicator shape to container.
     */
    sizeRatio: PropTypes.number,
    /**
     * Animation speed multiplier.
     */
    speed: PropTypes.number,
    /**
     * Pause the animation.
     */
    paused: PropTypes.bool,
    /**
     * Render with circular container background.
     */
    contained: PropTypes.bool,
    /**
     * Container background when contained.
     */
    containerColor: PropTypes.string,
};

export default M3LoadingIndicator;
