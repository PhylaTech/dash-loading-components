import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import { M3LoadingIndicator as Upstream } from '@alerix/m3-loading-indicator/react';

/**
 * M3LoadingIndicator — Dash wrapper for upstream spinner.
 */
const M3LoadingIndicator = (props) => {
    const {id, className, style, size, color, size_ratio, speed, paused, contained, container_color, playing} = props;
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            <Upstream size={size} color={color} sizeRatio={size_ratio} speed={speed} paused={paused} contained={contained} containerColor={container_color} {...contract('m3', 'M3LoadingIndicator', props)} />
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
    size_ratio: PropTypes.number,
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
    container_color: PropTypes.string,
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

export default M3LoadingIndicator;
