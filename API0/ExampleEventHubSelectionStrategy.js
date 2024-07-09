'use strict';

// Ensure the correct package is imported
         
import { AbstractEventHubSelectionStrategy } from 'fabric-network';

class ExampleEventHubSelectionStrategy extends AbstractEventHubSelectionStrategy {

    constructor(peers) {
        super();
        this.peers = peers;
        this.disconnectedPeers = [];
        this.cleanupInterval = null;
    }

    _disconnectedPeerCleanup() {
        this.cleanupInterval = setInterval(() => {
            // Reset the list of disconnected peers every 10 seconds
            for (const peerRecord of this.disconnectedPeers) {
                // If 10 seconds has passed since the disconnect
                if (Date.now() - peerRecord.time > 10000) {
                    this.disconnectedPeers = this.disconnectedPeers.filter((p) => p !== peerRecord.peer);
                }
            }

            if (this.disconnectedPeers.length === 0) {
                clearInterval(this.cleanupInterval);
                this.cleanupInterval = null;
            }
        }, 10000);
    }

    /**
     * Returns the next peer in the list per the strategy implementation
     * @returns {ChannelPeer}
     */
    getNextPeer() {
        // Convert disconnectedPeers to a Set for faster lookups
        const disconnectedPeersSet = new Set(this.disconnectedPeers);

        // Only select those peers that are not in the disconnectedPeers Set
        let availablePeers = this.peers.filter((peer) => !disconnectedPeersSet.has(peer));
        if (availablePeers.length === 0) {
            availablePeers = this.peers;
        }
        const randomPeerIdx = Math.floor(Math.random() * availablePeers.length);
        return availablePeers[randomPeerIdx];
    }

    /**
     * Updates the status of a peers event hub
     * @param {ChannelPeer} deadPeer The peer that needs its status updating
     */
    updateEventHubAvailability(deadPeer) {
        if (!this.cleanupInterval) {
            this._disconnectedPeerCleanup();
        }
        this.disconnectedPeers.push({ peer: deadPeer, time: Date.now() });
    }
}

module.exports = ExampleEventHubSelectionStrategy;