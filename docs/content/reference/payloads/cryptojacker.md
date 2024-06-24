---
title: "Cryptojacker"
draft: false
description: "Reference material for the Cryptojacker payload"
pre: "<i class='fa fa-coins'></i> "
---
{{< table_of_contents >}}

## Configuration

<!--
This documentation was autogenerated by passing the plugin's config-schema.json
through https://github.com/adobe/jsonschema2md. It was then modified by hand to
remove extraneous information.
-->

| Property                                                                                | Type      | Required | Nullable       |
| :-------------------------------------------------------------------------------------- | :-------- | :------- | :------------- |
| [duration](#duration)                                                                   | `number`  | Optional | cannot be null |
| [cpu\_utilization](#cpu_utilization)                                                    | `number`  | Optional | cannot be null |
| [memory\_utilization](#memory_utilization)                                              | `number`  | Optional | cannot be null |
| [simulate\_bitcoin\_mining\_network\_traffic](#simulate_bitcoin_mining_network_traffic) | `boolean` | Optional | cannot be null |

### duration

The duration (in seconds) for which the cryptojacking simulation should run on each machine.

`duration`

* is optional

* Type: `number`

* cannot be null

#### duration Type

`number`

#### duration Constraints

**minimum**: the value of this number must greater than or equal to: `0`

#### duration Default Value

The default value is:

```json
300
```

### cpu\_utilization

The percentage of CPU to use on a machine. The cryptojacker will use this percentage of a single CPU core.

`cpu_utilization`

* is optional

* Type: `number`

* cannot be null

#### cpu\_utilization Type

`number`

#### cpu\_utilization Constraints

**maximum**: the value of this number must smaller than or equal to: `100`

**minimum**: the value of this number must greater than or equal to: `0`

#### cpu\_utilization Default Value

The default value is:

```json
80
```

### memory\_utilization

The percentage of memory to use on a machine. An internal safeguard prevents more than 90% of the available RAM from being consumed, even if a higher percentage is specified.

`memory_utilization`

* is optional

* Type: `number`

* cannot be null

#### memory\_utilization Type

`number`

#### memory\_utilization Constraints

**maximum**: the value of this number must smaller than or equal to: `100`

**minimum**: the value of this number must greater than or equal to: `0`

#### memory\_utilization Default Value

The default value is:

```json
20
```

### simulate\_bitcoin\_mining\_network\_traffic

If enabled, the Agent will periodically send `getblocktemplate` requests used in Bitcoin mining over the network via HTTP.

`simulate_bitcoin_mining_network_traffic`

* is optional

* Type: `boolean`

* cannot be null

#### simulate\_bitcoin\_mining\_network\_traffic Type

`boolean`