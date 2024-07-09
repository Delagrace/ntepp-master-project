/*
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const FabricCAServices = require('fabric-ca-client');
const { FileSystemWallet, Gateway, X509WalletMixin, DefaultEventHandlerStrategies, GatewayOptions} = require('fabric-network');
const fs = require('fs');
const path = require('path');
//const ExampleEventHubSelectionStrategy = require('./ExampleEventHubSelectionStrategy');

const ccpPath = path.resolve(__dirname, 'connection.json');
const ccpJSON = fs.readFileSync(ccpPath, 'utf8');
const ccp = JSON.parse(ccpJSON);

class FabricService {

    async enrollAdmin(adminName, password) {
        try {
            const caURL = ccp.certificateAuthorities['ca-org1'].url;
            const ca = new FabricCAServices(caURL);
            const walletPath = path.join(process.cwd(), 'wallet');
            await this.ensureDirectoryExists(walletPath);
            const wallet = new FileSystemWallet(walletPath);
            console.log(`Wallet path: ${walletPath}`);

            const adminExists = await wallet.exists(adminName);
            if (adminExists) {
                console.log(`An identity for the admin user "${adminName}" already exists in the wallet`);
                return;
            }

            const enrollment = await ca.enroll({ enrollmentID: adminName, enrollmentSecret: password });
            const identity = X509WalletMixin.createIdentity('Org1MSP', enrollment.certificate, enrollment.key.toBytes());
            wallet.import(adminName, identity);
            console.log(`Successfully enrolled admin user "${adminName}" and imported it into the wallet`);
            return identity;
        } catch (error) {
            console.error(`Failed to enroll admin user "${adminName}": ${error}`);
            return error;
        }
    }

    async ensureDirectoryExists(directory) {
        try {
            await fs.promises.access(directory);
        } catch (error) {
            if (error.code === 'ENOENT') {
                await fs.promises.mkdir(directory, { recursive: true });
            } else {
                throw error;
            }
        }
    }

    async registerUser(adminName, username) {
        try {
            const walletPath = path.join(process.cwd(), 'wallet');
            const wallet = new FileSystemWallet(walletPath);
            console.log(`Wallet path: ${walletPath}`);

            const userExists = await wallet.exists(username);
            if (userExists) {
                console.log(`An identity for the user "${username}" already exists in the wallet`);
                return;
            }

            const adminExists = await wallet.exists(adminName);
            if (!adminExists) {
                console.log(`An identity for the admin user "${adminName}" does not exist in the wallet`);
                console.log('Run the enrollAdmin.js application before retrying');
                return;
            }

            const gateway = new Gateway();
            await gateway.connect(ccp, { wallet, identity: adminName, discovery: { enabled: false } });

            const ca = gateway.getClient().getCertificateAuthority();
            const adminIdentity = gateway.getCurrentIdentity();

            const secret = await ca.register({ affiliation: 'org1.department1', enrollmentID: username, role: 'client' }, adminIdentity);
            const enrollment = await ca.enroll({ enrollmentID: username, enrollmentSecret: secret });
            const userIdentity = X509WalletMixin.createIdentity('Org1MSP', enrollment.certificate, enrollment.key.toBytes());
            wallet.import(username, userIdentity);
            console.log(`Successfully registered and enrolled admin user "${username}" and imported it into the wallet`);
            return userIdentity;
        } catch (error) {
            console.error(`Failed to register user "${username}": ${error}`);
            return error;
        }
    }

    async registerSensor(username, channel, smartcontract, args) {
        try {
            const walletPath = path.join(process.cwd(), 'wallet');
            const wallet = new FileSystemWallet(walletPath);
            console.log(`Wallet path: ${walletPath}`);

            const userExists = await wallet.exists(username);
            if (!userExists) {
                console.log(`An identity for the user "${username}" does not exist in the wallet`);
                console.log('Run the registerUser.js application before retrying');
                return;
            }
            let connectionOptions = {
                identity: username,
                wallet: wallet,
                discovery: { enabled: false, asLocalhost: false },
                eventHandlerOptions: {
                    commitTimeout: 20,
                    strategy: DefaultEventHandlerStrategies.MSPID_SCOPE_ANYFORTX
                },
            }
            const gateway = new Gateway();
            await gateway.connect(ccp, connectionOptions);

            const network = await gateway.getNetwork(channel);
            const contract = network.getContract(smartcontract);

            await contract.submitTransaction('registerSensor', args.sensorID);
            console.log(`${new Date().toISOString()} - Transaction has been submitted`);

            await gateway.disconnect();
            return 'Sensor registered';
        } catch (error) {
            console.error(`Failed to submit transaction: ${error}`);
            return error;
        }
    }

    async addTemp(username, channel, smartcontract, args) {
        try {
            const walletPath = path.join(process.cwd(), 'wallet');
            const wallet = new FileSystemWallet(walletPath);
            console.log(`Wallet path: ${walletPath}`);

            const userExists = await wallet.exists(username);
            if (!userExists) {
                console.log(`An identity for the user "${username}" does not exist in the wallet`);
                console.log('Run the registerUser.js application before retrying');
                return;
            }

            let connectionOptions = {
                identity: username,
                wallet: wallet,
                discovery: { enabled: false, asLocalhost: false },
                eventHandlerOptions: {
                    commitTimeout: 30,
                    strategy: DefaultEventHandlerStrategies.MSPID_SCOPE_ANYFORTX
                },
            }
            const gateway = new Gateway();
            await gateway.connect(ccp, connectionOptions);

            const network = await gateway.getNetwork(channel);
            const contract = network.getContract(smartcontract);

            await contract.submitTransaction('addTemp', args.sensorID, args.kwh, args.time, args.gps, args.voltage, args.pf);
            console.log(`${new Date().toISOString()} - Transaction has been submitted`);

            await gateway.disconnect();
            return 'Transaction has been submitted';
        } catch (error) {
            console.error(`Failed to submit transaction: ${error}`);
            return error;
        }
    }

    async getHistory(username, channel, smartcontract, args) {
        try {
            const walletPath = path.join(process.cwd(), 'wallet');
            const wallet = new FileSystemWallet(walletPath);
            console.log(`Wallet path: ${walletPath}`);

            const userExists = await wallet.exists(username);
            if (!userExists) {
                console.log(`An identity for the user "${username}" does not exist in the wallet`);
                console.log('Run the registerUser.js application before retrying');
                return;
            }
            let connectionOptions = {
                identity: username,
                wallet: wallet,
                discovery: { enabled: false, asLocalhost: false },
                eventHandlerOptions: {
                    commitTimeout: 20,
                    strategy: DefaultEventHandlerStrategies.MSPID_SCOPE_ANYFORTX
                },
            }
            const gateway = new Gateway();
            await gateway.connect(ccp, connectionOptions);

            const network = await gateway.getNetwork(channel);
            const contract = network.getContract(smartcontract);

            const result = await contract.evaluateTransaction('getHistory', args.sensorID);
            console.log(`${new Date().toISOString()} - Transaction has been evaluated, result is: ${result.toString()}`);
            return result.toString();
        } catch (error) {
            console.error(`Failed to evaluate transaction: ${error}`);
            return error;
        }
    }
}

module.exports = FabricService;
