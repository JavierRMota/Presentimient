/*! \file psyreg.h
    \brief Include this header for access to all API functionality.

	For interacting with the PsyREG API in Visual Basic applications, see PsyREG.vb in the sample modules.
	Copyright 2008 Psyleron, Inc.
*/

#ifndef _PSYREG_H_
#define _PSYREG_H_

/*! \cond */
#ifdef PSYREG_EXPORTS
#define PSYREG_API __declspec(dllexport)
#else
#define PSYREG_API __declspec(dllimport)
#endif
/*! \endcond */

/*! \cond */
typedef int DataSource;
/*! \endcond */

typedef int BOOL;	/*!< Boolean type for C clients. Value can be either TRUE or FALSE */

#ifndef TRUE
#define TRUE 1	/*!< C value for BOOL type*/
#endif

#ifndef FALSE
#define FALSE 0	/*!< C value for BOOL type*/
#endif

/*!	Status value for a DataSource.*/
/*! Contains logically-OR'd bit-flag values named BSS_*
	\sa BSS_GOOD
*/
typedef unsigned long bs_status;

const int PSYREG_API_VERSION = 1;				/*!< Version of the API that this header is indended for. Should be compared to PsyREGAPIVersion() */

const DataSource INVALID_DATASOURCE = -1;		/*!< Constant representing an invalid Datasource */

const bs_status BSS_GOOD			= 0x0000;	/*!< no flags set. the device is ok and there are no problems */
const bs_status BSS_CONNECTING		= 0x0001;	/*!< device connection is being established (in the process of opening) */
const bs_status BSS_WAITING			= 0x0002;	/*!< waiting for device data (buffer empty) */
const bs_status BSS_BUSY			= 0x0004;	/*!< device is in use by another application */
const bs_status BSS_NODEVICE		= 0x0008;	/*!< there is no device by this name connected anymore */
const bs_status BSS_READERROR		= 0x0010;	/*!< was there a read error during the last read */
const bs_status BSS_BADCFG			= 0x0020;	/*!< was there a bad configuration for the device (e.g. conflicting values or unset values) */
const bs_status BSS_CANTPROCESS		= 0x0040;	/*!< was there a processing error? [set at bitsource level] */
const bs_status BSS_INITERROR		= 0x0080;	/*!< was there an initialization error / problem with the data structure [set at bitsource level] */
const bs_status BSS_TIMEOUT			= 0x0100;	/*!< did the reader time out since the last device read [set at bitsource level] */
const bs_status BSS_GENERALERROR	= 0x8000;	/*!< was there any error at all. set if any other error (busy, nodevice, readerror, cantprocess) [set at bitsource level] */
const bs_status BSS_INVALID			= 0x0200;	/*!< is the DataSource invalid. This occurs when a DataSource was not created or has already been destroyed. */

#ifdef __cplusplus
extern "C" {
#endif

	/*!	Returns a version number for this build of the API DLL */
	/*!	Use this methods before starting an application to ensure that the version being used is the same one that the client was written for.
		For Example: compare PsyREGAPIVersion and PSYREG_API_VERSION
		\sa PSYREG_API_VERSION
	*/
	PSYREG_API int PsyREGAPIVersion();

	/*!	Returns the build number of this API DLL */
	/*!	This is mainly a development tool, used for debugging version problems and tracking bugs. When bugs or other issues arise with this API, the build number
		will be needed for technical support or bug reporting.
	*/
	PSYREG_API unsigned long PsyREGAPIBuild();

	/*!	Searches for connected hardware data sources and adds them to an internal list. */
	/*! Currently, only devices of the type REG-1 will be enumerated. Individual sources will not be enumerated if they are in use by a different application.
		Returns the number of new sources found during this enumeration. This value can be 0. Returns -1 on error. GetSourceCount will then return the size of the
		internal list and GetSource will provide client access to sources in the list.
		This function can be called numerous time without affecting outstanding DataSource handles as it does NOT remove any source from the list regardless of their
		state. Disconnected sources must be removed from the list by calling ClearSources, which has special conditions.
		\warning This function may block for any amount of time betweeen 0 and one half seconds depending on how many devices are enumerated. Keep that in mind if
		calling during a real-time application.
		\sa GetSourceCount
		\sa ClearSources
	*/
	PSYREG_API int PsyREGEnumerateSources();

	/*!	Returns the number of sources stored in the internal list built by one or more calls to EnumerateSources. */
	/*! Each source is then accessible by calling GetSource with an index greater than or equal to 0 and less than this return value.
		\sa EnumerateSources
	*/
	PSYREG_API unsigned int PsyREGGetSourceCount();

	/*!	Clears the entire list of sources built by one or more calls to EnumerateSources */
	/*! This function should be called before shuttind down an application. This function may also be called as the first step to re-enumerate sources. Since
		EnumerateSources does not clear sources already on the list or check their status, this function may be neccesary to remove source from the internal list
		when they are no longer valid (i.e. disconnected or used by another applicaton).
		\warning This function should not be called if there are any outstanding datasources. All sources that were opened must be closed and released. Errors
		may occur if these conditions are not met.
		\sa EnumerateSources
	*/
	PSYREG_API void PsyREGClearSources();

	/*!	Retreives the handle to a datasource based on its index in a list of sources */
	/*! This method is used to access the sources found in EnumerateSources. Whether actually reading data or just inspecting the enumerated sources, this
		function will return a DataSource handle to serve that purpose. This DataSource handle does not 'lock' the source in any way. The Datasource returned
		may be disbanded at any time if unused. GetDeviceType and GetDeviceId may be called at any time using the returned source, which provides a simple way
		to list all sources.
		\sa GetSourceCount
		\sa GetDeviceType
		\sa GetDeviceId
		\sa Open
		\sa ReleaseSource
	*/
	PSYREG_API DataSource PsyREGGetSource(unsigned int uiIndex);

	/*!	Releases a given source back to the source manager. */
	/*! This should be called when a source retrieved with GetSource is no longer needed.
		After releasing, the caller should set unused source variables to INVALID_DATASOURCE.
		\sa GetSource
		\sa Close
	*/
	PSYREG_API void PsyREGReleaseSource(DataSource source);

	/*!	Begins opening a DataSource for interaction */
	/*! Before data can be read from a DataSource, its (hardware) device must be opened for access. Currently, this is instantaneous, but in the future
		certain device types may have long connecting (opening) processes. This process will happen asyncronously, and the status of this DataSource will
		have its BS_CONNECTING bit set. When that bit is no longer set, this process is complete and Opened should return true. If Opened returns false
		at that time, there was an error which may be explained by other status flags.
		\return true if the DataSource was able to begin opening, false if not.
		\sa Opened
		\sa Close
	*/
	PSYREG_API BOOL PsyREGOpen(DataSource source);

	/*!	Closes an open DataSource and prevents further interaction. */
	/*! When done with a source, it must be closed. This prevents allows other applications to begin using the device associated with this DataSource.
		If this function is not called when a source is no longer used, that source will be inaccessible by other applications until the module that
		implements these functions is unloaded.
		Following Close, a DataSource still exists and must be released with ReleaseSource.
		\sa ReleaseSource
	*/
	PSYREG_API void PsyREGClose(DataSource source);

	/*!	Signals that the data in the DataSource internal buffer is stale and performs a clear. */
	/*! Typically, the DataSource will refresh its own internal buffer when it becomes stale. Therefore, calling this function is almost always
		not necessary. This function will always succeed.
	*/
	PSYREG_API void PsyREGReset(DataSource source);

	/*!	Checks if the DataSource has been opened or not. If opened, a DataSource is ready to be read from */
	/*! A DataSource should be open immediately after successfully calling Open. In future versions, certain devices may have a long
		connecting sequence. In those cases, Open will return true, but Opened will return false until the device has completed its connecting process.
		The DataSource status will have the BS_CONNECTING flag set durring the connecting process until the device is open or failed to open.
		\return true if the DataSource is currently open, false if not.
	*/
	PSYREG_API BOOL PsyREGOpened(DataSource source);

	/*!	Returns a status value containing various OR'd bit-flags representing the current state of DataSource represented by a DataSource. */
	/*!	If BS_INVALID is set in the result value, then this DataSource is not valid. If the BS_GENERALERROR is set, then there has been a device access
		error and no more data will be read from this DataSource. It should be Closed. After that, another Open may be attempted, but is unlikely to work
		unless there has been a change in the physical state of the device (e.g. an REG-1 was unplugged then plugged back in).
		\return a bs_status containing OR'd bit-flags representing the current device status.
	*/
	PSYREG_API bs_status PsyREGGetStatus(DataSource source);
	
	/*!	Returns a string representing the type of connected device represented by a DataSource. */
	/*!	If the returned string is empty, the DataSource is not valid.
		The type will be placed in szBuf, which the caller must provide. It should be atleast 64 bytes.
		\return a null-terminated const char array containing the device type.
	*/
	PSYREG_API const char* PsyREGGetDeviceType(DataSource source, char* szBuf);

	/*!	Version of PsyREGGetDeviceType for <b>Visual Basic</b>. */
	/*! Returns a System-Allocated BSTR
	*/
	PSYREG_API unsigned short* PsyREGGetDeviceTypeBSTR(DataSource source);

	/*!	Returns a string representing the identity of connected device represented by a DataSource. */
	/*!	If the returned string is empty, the DataSource is not valid.
		The id will be placed in szBuf, which the caller must provide. It should be atleast 64 bytes.
		\return a null-terminated const char array containing the device identity.
	*/
	PSYREG_API const char* PsyREGGetDeviceId(DataSource source, char* szBuf);

	/*!	Version of PsyREGGetDeviceId for <b>Visual Basic</b>. */
	/*! Returns a System-Allocated BSTR
	*/
	PSYREG_API unsigned short* PsyREGGetDeviceIdBSTR(DataSource source);

	/*!	Retrieves a single bit from the datasource stream queue. */
	/*!	Requires an Open Datasource. Result will be placed into LSB of pucBuf. Other bits in the first byte of pucBuf may be overwritten.
		If this function fails, check GetStatus to see if there is a source error.
		\return true if a bit was placed into ucBuf, false otherwise. 
		\sa GetByte
		\sa GetBits
		\sa GetBytes
		\sa GetStatus
	*/
	PSYREG_API BOOL PsyREGGetBit(DataSource source, unsigned char* pucBuf);

	/*!	Retrieves a full byte from the datasource stream queue. */
	/*!	Requires an Open Datasource. Resultint 8 bits will be packed into pucBuf. If this function fails, check GetStatus to see if there is a source error.
		\return true if a bit was placed into ucBuf, false otherwise. 
		\sa GetByte
		\sa GetBits
		\sa GetBytes
		\sa GetStatus
	*/
	PSYREG_API BOOL PsyREGGetByte(DataSource source, unsigned char* pucBuf);

	/*!	Retrieves a block of bits from the datasource stream queue. This function will dequeue some number of bits up to iMaxBits depending on the state of the internal buffer. */
	/*!	Requires an Open Datasource. Results will be placed into pucBuf with the oldest data at offset 0. Each byte in the result buffer will have its LSB set
		to 0 or 1. If the datasource stream buffer does not have enough data to satisfy the request, only the available data will be returned. If this function
		fails, check GetStatus to see if there is a source error. The recommended way of accumulating a large buffer full of bits using GetBits is to periodically
		call this function with bBlock = FALSE, and append the retrieved data from each call onto your own buffer. Perform your program logic between calls. bBlock=FALSE
		will provide the most responsive application since this function will not block. If you wish to wait for a full dataset of iMaxBits, set bBlock=TRUE. This
		function will then block indefinitely until iMaxBits data bits have been placed into the buffer or until there is some device error.
		\return the number of bytes placed in pucBuf (where each byte contains 1 bit). Returns 0 on failure.
		\note For <b>Visual Basic</b>
			When calling this function, the pucBuf parameter must be the reference of the first element in the VB ByteArray.
		\sa GetBit
		\sa GetBits
		\sa GetBytes
		\sa GetStatus
	*/
	PSYREG_API int PsyREGGetBits(DataSource source, unsigned char* pucBuf, int iMaxBits, BOOL bBlock);

	/*!	Retrieves a block of bytes from the datasource stream queue. This function will dequeue some number of bytes up to iMaxBytes depending on the state of the internal buffer. */
	/*!	Requires an Open Datasource. Results will be placed into pucBuf with the oldest data at offset 0. Each byte in the result buffer be packed with 8 bits.
		If the datasource stream buffer does not have enough data to satisfy the request, only the available data will be returned. If this function
		fails, check GetStatus to see if there is a source error. The recommended way of accumulating a large buffer full of bytes using GetBytes is to periodically
		call this function with bBlock = FALSE, and append the retrieved data from each call onto your own buffer. Perform your program logic between calls. bBlock=FALSE
		will provide the most responsive application since this function will not block. If you wish to wait for a full dataset of iMaxBytes, set bBlock=TRUE. This
		function will then block indefinitely until iMaxBytes data bytes have been placed into the buffer or until there is some device error.
		\return the number of bytes placed in pucBuf (where each byte contains 8 bits). Returns 0 on failure.
		\note For <b>Visual Basic</b>
			When calling this function, the pucBuf parameter must be the reference of the first element in the VB ByteArray.
		\sa GetBit
		\sa GetByte
		\sa GetBits
		\sa GetStatus
	*/
	PSYREG_API int PsyREGGetBytes(DataSource source, unsigned char* pucBuf, int iMaxBytes, BOOL bBlock);

#ifdef __cplusplus
}
#endif

#endif